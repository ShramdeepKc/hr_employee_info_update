# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployeeChange(models.Model):
    _name = 'hr.employee.change'
    _description = 'Employee Information Change Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Fields to store employee change request details
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    field_name = fields.Selection([
        ('name', 'Name'),
        ('work_email', 'Work Email'),
        ('mobile_phone', 'Mobile Phone'),
    ], string='Field to Change', required=True)
    current_value = fields.Char(string='Current Value')
    new_value = fields.Char(string='New Value', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    # Automatically set the current value based on selected employee and field
    @api.onchange('employee_id', 'field_name')
    def _onchange_field_name(self):
        if self.employee_id and self.field_name:
            self.current_value = getattr(self.employee_id, self.field_name)

    # Method to submit the change request for approval
    def action_submit(self):
        self.state = 'submitted'
        self._notify_admin()

    # Method to approve the change request and update the employee's information
    def action_approve(self):
        self.state = 'approved'
        setattr(self.employee_id, self.field_name, self.new_value)
        self._notify_employee('approved')

    # Method to reject the change request
    def action_reject(self):
        self.state = 'rejected'
        self._notify_employee('rejected')

    # Helper method to notify the admin about the new change request
    def _notify_admin(self):
        template = self.env.ref('hr_employee_info_update.email_template_change_request_admin')
        for admin in self.env.ref('hr.group_hr_manager').users:
            template.send_mail(self.id, force_send=True, email_values={'email_to': admin.partner_id.email})

    # Helper method to notify the employee about the result of their change request (approved/rejected)
    def _notify_employee(self, action):
        template = self.env.ref(f'hr_employee_info_update.email_template_change_request_{action}')
        template.send_mail(self.id, force_send=True)
