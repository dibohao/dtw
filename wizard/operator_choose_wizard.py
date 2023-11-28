from odoo import models, fields, api
from odoo import exceptions # will be used in the code
import logging
_logger = logging.getLogger(__name__)

class OperatorWizard(models.TransientModel):
    _name = 'dtw.operator.wizard'
    
    operator_id=fields.Many2one('res.users')

    def operator_action(self):
        active_id=self.env.context['active_id']
        active_model=self.env.context['active_model']
        self.env['dtw.workmanship.main'].update_dispatch()
        self.env['dtw.workmanship'].search([('dispatch','=',True)]).update({'operator_id':self.operator_id.id})
        self.env[active_model].browse(active_id).state='to_excel'