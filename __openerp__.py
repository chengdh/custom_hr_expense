# -*- coding: utf-8 -*-

{
    'name': 'custom hr expense',
    'version': '0.1',
    'category': 'Human Resources',
    'description': """定制hr.expense-for ktv""",
    'author': 'chengdh (cheng.donghui@gmail.com)',
    'website': '',
    'license': 'AGPL-3',
    'depends': ['hr_expense','web'],
    'data': [
      "hr_expense_view.xml",
      "hr_expense_workflow.xml",
      "hr_expense_data.xml",
      "security/hr_expense_secure.xml",
      "report.xml",
      ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'web':True,
    'css': [],
    'js': [],
    'xml': [],
}

