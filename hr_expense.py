#coding: utf-8
#重写hr_expense,用于处理手机上的数据获取
from openerp.osv import fields, osv
import math
from datetime import datetime
from openerp.tools.translate import _
import openerp.tools as tools
import logging

_logger = logging.getLogger(__name__)

class hr_expense(osv.osv):
  '''
  费用
  '''
  _name = "hr.expense.expense"
  _inherit = 'hr.expense.expense'
  _description = "hr expense custom"

  _track = {
    'state': {
        'custom_hr_expense.mt_expense_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'accepted',
        'custom_hr_expense.mt_expense_refused': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'cancelled',
        'custom_hr_expense.mt_expense_confirmed': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'confirm',
        'custom_hr_expense.mt_expense_dept_manager_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'dept_manager_approved',
        'custom_hr_expense.mt_expense_shop_manager_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'shop_manager_approved',
        'custom_hr_expense.mt_expense_vice_general_manager_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'vice_general_manager_approved',
        'custom_hr_expense.mt_expense_ceo_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'ceo_approved',
        'custom_hr_expense.mt_expense_hr_manager_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'hr_manager_approved',
        'custom_hr_expense.mt_expense_stock_manager_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'stock_manager_approved',
      },
    }


  def _get_where_args_with_workflow(self,cr,uid):
    '''
    获取当前用户工作流审批相关的where 条件
    '''
    matched_groups = None
    pool = self.pool.get('res.users')
    user = pool.browse(cr,uid,uid)
    groups = user.groups_id
    if not groups: return None 
    #根据group_id获取group名称
    model_data_pool = self.pool.get("ir.model.data")
    #部门经理
    group_dept_manager = model_data_pool.get_object(cr,uid,'base','group_dept_manager')
    #店长
    group_shop_manager = model_data_pool.get_object(cr,uid,'base','group_shop_manager')
    #库管
    group_stock_manager = model_data_pool.get_object(cr,uid,'stock','group_stock_manager')
    #人力资源经理
    group_hr_manager = model_data_pool.get_object(cr,uid,'base','group_hr_manager')
    #财务经理
    group_account_manager = model_data_pool.get_object(cr,uid,'base','group_account_manager')
    #副总
    group_general_manager = model_data_pool.get_object(cr,uid,'base','group_vice_general_manager')
    #总经理
    group_ceo = model_data_pool.get_object(cr,uid,'base','group_ceo')

    #找出当前用户属于哪个group
    list_b = [group_dept_manager,group_shop_manager,group_general_manager,group_ceo,group_hr_manager,group_stock_manager]
    matched_groups = list(set(groups).intersection(set(list_b)))
    if not matched_groups: return None

    if group_ceo in matched_groups:
      state = ["dept_manager_approved","vice_general_manager_approved","hr_manager_approved"]
      signal = "ceo_approve"

    if group_general_manager in matched_groups:
      state = ["shop_manager_approved"]
      signal = "vice_general_manager_approve"

    if group_shop_manager in matched_groups:
      state = ["subed_1","subed_3"]
      signal = "shop_manager_approve"

    if group_dept_manager in matched_groups:
      state = ["subed_2"]
      signal = "dept_manager_approve"

    if group_hr_manager in matched_groups:
      state = ["stock_manager_approved"]
      signal = "hr_manager_approve"

    if group_stock_manager in matched_groups:
      state = ["shop_manager_approved"]
      signal = "stock_manager_approve"


    return {"state" : state,"signal" : signal}

  def _next_workflow_signal(self,cr,uid, ids, field_name, arg, context):
    res = {}
    #获取当前用户能查看的expense的状态
    where_args = self._get_where_args_with_workflow(cr,uid)
    for record in self.browse(cr,uid,ids,context):
      res[record.id] = None
      if record.state in where_args['state']: res[record.id] = where_args['signal']

    return res

  _columns = {
      'state': fields.selection([
        ('draft', 'draft'),                                                           #草稿
        ('cancelled', 'refused'),                                                   #已驳回
        ('confirm',  'confirmed'),                                                   #已确认
        ('accepted',  'accepted'),                                                  #部门经理已审批
        ('subed_1',  'subflow 1'),                                                  #部门经理已审批
        ('subed_2',  'subflow 2'),                                                  #部门经理已审批
        ('subed_3',  'subflow 3'),                                                  #部门经理已审批
        ('shop_manager_approved',  'Shop manager approved'),
        ('dept_manager_approved',  'Dept manager approved'),
        ('vice_general_manager_approved',  'Vice general manager approved'),
        ('stock_manager_approved',  'Stock manager approved'),
        ('hr_manager_approved',  'Hr manager approved'),
        ('ceo_approved',  'CEO approved'),
        ('done','waitting payment'),
        ('paid','paid'),
        ],
        'Status', readonly=True, track_visibility='onchange',
        help='When the expense request is created the status is \'Draft\'.\n It is confirmed by the user and request is sent to admin, the status is \'Waiting Confirmation\'.\
            \nIf the admin accepts it, the status is \'Accepted\'.\n If the accounting entries are made for the expense request, the status is \'Waiting Payment\'.'),

      "next_workflow_signal" : fields.function(_next_workflow_signal,string="根据当前用户计算下一个workflow signal"),
      }

  def get_waiting_audit_expenses(self,cr,uid,context=None):
    #FIXME 为简单处理,此处为硬编码 
    #1 根据uid获取用户所属group_id
    #2 根据group_id找出对应的工作流state
    #3 根据state获取expense列表,返回客户端
    where_args = self._get_where_args_with_workflow(cr,uid)
    if not where_args : return []

    _logger.debug("[state,signal] = " + repr(where_args));
    _logger.debug("context = " + repr(context));
    ids = self.search(cr,uid,[("state","in",where_args['state'])])
    _logger.debug("ids = " + repr(ids));
    if not ids: return []
    expenses = self.read(cr,uid,ids,context=context)
    _logger.debug("return expenses =  " + repr(expenses));
    return expenses
