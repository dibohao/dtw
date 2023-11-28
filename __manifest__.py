# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': '智能扭矩系统',
    'category': '智能扭矩系统',
    'summary': '数字扭力扳手管理模块',
    'version': '16.0',
    'website': '',
    'author': 'dibohao',
    'depends': ['base','report_xlsx'],
    'data': [
        'security/dtw_groups.xml',
        'security/ir.model.access.csv',
        'views/menu_action.xml',
        'views/dtw_view.xml',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',
        'wizard/operator_choose_view_wizard.xml'
    ],
    'qweb': [],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'sequence': 10,
    "application": True,
}