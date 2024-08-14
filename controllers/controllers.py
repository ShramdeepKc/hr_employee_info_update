# -*- coding: utf-8 -*-
# from odoo import http


# class HrEmployeeInfoUpdate(http.Controller):
#     @http.route('/hr_employee_info_update/hr_employee_info_update', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_employee_info_update/hr_employee_info_update/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_employee_info_update.listing', {
#             'root': '/hr_employee_info_update/hr_employee_info_update',
#             'objects': http.request.env['hr_employee_info_update.hr_employee_info_update'].search([]),
#         })

#     @http.route('/hr_employee_info_update/hr_employee_info_update/objects/<model("hr_employee_info_update.hr_employee_info_update"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_employee_info_update.object', {
#             'object': obj
#         })

