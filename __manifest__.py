# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': '数字扭力扳手管理',
    'category': '数字扭力扳手管理',
    'summary': '数字扭力扳手管理模块',
    'version': '16.0',
    'website': '',
    'author': 'dibohao',
    'depends': ['base'],
    'data': [
        'security/dtw_groups.xml',
        'security/ir.model.access.csv',
        'views/menu_action.xml',
        'views/dtw_view.xml',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml'
    ],
    'qweb': [],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'sequence': 10,
    "application": True,
}