# -*- coding: utf-8 -*-
from odoo import models, fields

# This class extends the hr.employee model to include a relationship with the change request model.
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # A one-to-many relationship to store all change requests associated with an employee.
    change_request_ids = fields.One2many('hr.employee.change', 'employee_id', string='Change Requests')

    # This method opens a form view to allow the employee to request an information change.
    def action_request_change(self):
        return {
            'name': 'Request Information Change',  # The name of the window that will open.
            'type': 'ir.actions.act_window',  # The action type to open a new window.
            'res_model': 'hr.employee.change',  # The model that the form view is based on.
            'view_mode': 'form',  # The view mode to use (form view in this case).
            'context': {'default_employee_id': self.id},  # Default context to pre-fill the employee field.
            'target': 'new',  # Opens the form in a new window.
        }
