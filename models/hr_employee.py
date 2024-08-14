# -*- coding: utf-8 -*-
from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # One2many field to link employee with their change requests
    change_request_ids = fields.One2many('hr.employee.change', 'employee_id', string='Change Requests')

    # Action to open a form view for creating a new change request
    def action_request_change(self):
        return {
            'name': 'Request Information Change',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee.change',
            'view_mode': 'form',
            'context': {'default_employee_id': self.id},  # Pre-fill the employee field in the form
            'target': 'new',  # Open the form in a new window
        }
#