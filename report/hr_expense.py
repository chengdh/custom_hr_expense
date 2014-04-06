#coding: utf-8
#hr.expense打印模板
import time
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import pooler
from netsvc import Service

def to_big_rmb(money=0,rmb=None):
    '''
    人民币小写转大写
    '''
    big = [u'零', u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖']  
    rmb = [u'分', u'角', u'圆', u'拾', u'佰', u'仟', u'万', u'拾', u'佰', u'仟', u'亿', u'拾', u'佰', u'仟', u'万',u'拾', u'佰', u'仟',u'万',u'亿']  
    if rmb:
        rmb = rmb

    #转成字符串
    str_money = str( int(money * 100) )[::-1]
    big_money = ''

    #拼大写金额
    for i in xrange(len(str_money)):
        n = ord(str_money[i]) - ord('0')
        big_money = big[n] + rmb[i] + big_money  

    #去掉零ls
    rule = (u'零仟', u'零',
            u'零佰', u'零',
            u'零拾', u'零',
            u'零亿', u'亿',
            u'零万', u'万',
            u'零元', u'元',
            u'零角', u'零',
            u'零分', u'零',
            u'零零', u'零',
            u'零亿', u'亿',
            u'零零', u'零',
            u'零万', u'万',
            u'零零', u'零',
            u'零圆', u'圆',
            u'亿万', u'亿',
            u'零', u'',
            u'圆$', u'圆整')

    for i in xrange(0,len(rule),2):
        big_money = big_money.replace(rule[i], rule[i+1])  

    return big_money

class expense(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(expense, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'to_big_rmb': to_big_rmb})

del Service._services['report.hr.expense']
report_sxw.report_sxw('report.hr.expense.new','hr.expense.expense','addons/custom_hr_expense/report/hr_expense.mako',parser=expense)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
