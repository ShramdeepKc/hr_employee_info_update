# -*- coding: utf-8 -*-
from odoo import models, fields, api


# This model represents an employee's request to change their personal information.
class HrEmployeeChange(models.Model):
    _name = 'hr.employee.change'
    _description = 'Employee Information Change Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # The employee who is requesting the change.
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)

    # The field of the employee's record that they want to change.
    field_name = fields.Selection([
        ('name', 'Name'),
        ('work_email', 'Work Email'),
        ('mobile_phone', 'Mobile Phone'),
    ], string='Field to Change', required=True)

    # The current value of the field that is being changed.
    current_value = fields.Char(string='Current Value')

    # The new value that the employee wants to update the field to.
    new_value = fields.Char(string='New Value', required=True)

    # The current status of the change request.
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    # Automatically update the current value of the field when the employee or field is changed.
    @api.onchange('employee_id', 'field_name')
    def _onchange_field_name(self):
        if self.employee_id and self.field_name:
            self.current_value = getattr(self.employee_id, self.field_name)

    # Submit the change request, changing its status to 'submitted' and notify the HR manager.
    def action_submit(self):
        self.state = 'submitted'
        self._notify_admin()

    # Approve the change request, updating the employee's record and notifying the employee.
    def action_approve(self):
        self.state = 'approved'
        setattr(self.employee_id, self.field_name, self.new_value)
        self._notify_employee('approved')

    # Reject the change request and notify the employee.
    def action_reject(self):
        self.state = 'rejected'
        self._notify_employee('rejected')

    # Notify the HR manager that a change request has been submitted.
    def _notify_admin(self):
        template = self.env.ref('hr_employee_info_update.email_template_change_request_admin')
        for admin in self.env.ref('hr.group_hr_manager').users:
            template.send_mail(self.id, force_send=True, email_values={'email_to': admin.partner_id.email})

    # Notify the employee of the approval or rejection of their request.
    def _notify_employee(self, action):
        template = self.env.ref(f'hr_employee_info_update.email_template_change_request_{action}')
        template.send_mail(self.id, force_send=True)
