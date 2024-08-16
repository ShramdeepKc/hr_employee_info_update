from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


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
        for admin in self.env.ref('hr.group_hr_manager').users:
            try:
                subject = _("New Employee Change Request from %s") % self.employee_id.name
                body_html = _(
                    """
                    <p>Dear Admin,</p>
                    <p>A new change request has been submitted by <strong>%s</strong>.</p>
                    <p>Field to change: <strong>%s</strong></p>
                    <p>New value: <strong>%s</strong></p>
                    <p>Please review and take necessary action.</p>
                    """
                ) % (self.employee_id.name, self.field_name, self.new_value)

                email_values = {
                    'email_to': admin.partner_id.email,
                    'subject': subject,
                    'body_html': body_html,
                    'email_from': self.env.user.email_formatted,
                }

                self.env['mail.mail'].create(email_values).send()
                _logger.info("Notification email sent to admin %s", admin.partner_id.email)
            except Exception as e:
                _logger.error("Failed to send email to admin %s: %s", admin.partner_id.email, str(e))

    # Helper method to notify the employee about the result of their change request (approved/rejected)
    def _notify_employee(self, action):
        try:
            subject = _("Your Change Request Has Been %s") % action.capitalize()
            body_html = _(
                """
                <p>Dear %s,</p>
                <p>Your request to change your <strong>%s</strong> has been <strong>%s</strong>.</p>
                <p>%s</p>
                """
            ) % (self.employee_id.name, self.field_name, action, _("Thank you for your patience."))

            email_values = {
                'email_to': self.employee_id.work_email,
                'subject': subject,
                'body_html': body_html,
                'email_from': self.env.user.email_formatted,
            }

            self.env['mail.mail'].create(email_values).send()
            _logger.info("Notification email sent to employee %s", self.employee_id.work_email)
        except Exception as e:
            _logger.error("Failed to send email to employee %s: %s", self.employee_id.work_email, str(e))