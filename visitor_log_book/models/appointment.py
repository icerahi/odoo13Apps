from odoo import fields,api,models,_

class Appointment(models.Model):
    _name = 'appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'appointment_date'

    @api.onchange('employee')
    def based_on_employee(self):
        result = self.env['visitor_log_book.employee'].search([('id', '=', self.employee.id)])
        if result:
            self.em_phone = result.phone
            self.email = result.email
            self.department = result.department.name
            self.position = result.position.name
            self.employee_id = result.employee_id

    @api.onchange('em_phone')
    def based_on_em_phone(self):
        result = self.env['visitor_log_book.employee'].search([('phone', '=', self.em_phone)])
        if result:
            self.employee = result.id
            self.email = result.email
            self.department = result.department.name
            self.position = result.position.name
            self.employee_id = result.employee_id

    @api.onchange('email')
    def based_on_email(self):
        result = self.env['visitor_log_book.employee'].search([('email', '=', self.email)])
        if result:
            self.employee = result.id
            self.em_phone = result.phone
            self.department = result.department.name
            self.position = result.position.name
            self.employee_id = result.employee_id

    @api.onchange('employee_id')
    def based_on_employee_id(self):
        result = self.env['visitor_log_book.employee'].search([('employee_id', '=', self.employee_id)])
        if result:
            self.employee = result.id
            self.email = result.email
            self.department = result.department.name
            self.position = result.position.name
            self.em_phone = result.phone


    employee = fields.Many2one('visitor_log_book.employee',string='Employee Name')
    employee_id = fields.Char(string='Employee ID',required='True')
    department = fields.Char(string='Department')
    position = fields.Char(string='Job Position')
    em_phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')

##### auto load visitor information

    @api.onchange('visitor')
    def based_on_visitor(self):
        result = self.env['visitor_log_book.visitor'].search([('id', '=', self.visitor.id)])
        if result:
            self.visitor_id = result.visitor_id
            self.company = result.company.name
            self.designation = result.designation.name
            self.vi_phone = result.phone
            self.nid = result.nid

    @api.onchange('vi_phone')
    def based_on_vi_phone(self):
        result=self.env['visitor_log_book.visitor'].search([('phone','=',self.vi_phone)])
        if result:
            self.visitor = result.id
            self.visitor_id = result.visitor_id
            self.company = result.company.name
            self.designation = result.designation.name
            self.nid = result.nid


    @api.onchange('visitor_id')
    def based_on_visitor_id(self):
        result = self.env['visitor_log_book.visitor'].search([('visitor_id', '=', self.visitor_id)])
        if result:
            self.visitor = result.id
            self.nid = result.nid
            self.company = result.company.name
            self.designation = result.designation.name
            self.vi_phone = result.phone


    visitor = fields.Many2one('visitor_log_book.visitor',string='Visitor Phone')
    visitor_id = fields.Char(string='Visitor ID',required=True)
    company = fields.Char(string='Company')
    designation = fields.Char(string='Designation')
    purpose = fields.Selection([('official','Official'),('personal','Personal')],default='official')
    nid = fields.Char(string='NID(National ID)')
    vi_phone = fields.Char(string='Visitor Name ')
    appointment_date=fields.Datetime(string='Appointment Date',required=True)
    state = fields.Selection([('pending','Pending'),('done','Done')])


        #auto checkin when click button with data.
    def checkin_from_appointment(self):

        for f in self:
            if f.state== 'pending':
                f.state='done'
            values={
                'visitor':f.visitor.id,
                'vi_phone':f.vi_phone,
                'company':f.company,
                'designation':f.designation,
                'nid':f.nid,
                'visitor_id':f.visitor_id,

                'desired_person':f.employee.id,
                'em_phone':f.em_phone,
                'email':f.email,
                'department':f.department,
                'position':f.position,
                'employee_id':f.employee_id,

            }
            new_checkin=f.env['visitor_log_book.checkinout'].create(values)
            context = dict(f.env.context)
            return {
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'visitor_log_book.checkinout',
                'res_id':new_checkin.id,
            }


    @api.model
    def create(self, vals_list):
        result = super(Appointment, self).create(vals_list)
        result['state'] = 'pending'
        return result











