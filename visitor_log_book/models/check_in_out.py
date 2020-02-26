from odoo import models,fields,api,_
from datetime import datetime

class CheckInOut(models.Model):
    _name='visitor_log_book.checkinout'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'vi_phone'

    @api.onchange('visitor')
    def based_on_visitor(self):
        result = self.env['visitor_log_book.visitor'].search([('id','=',self.visitor.id)])
        if result:
            self.visitor_id=result.visitor_id
            self.company = result.company.name
            self.designation = result.designation.name
            self.vi_phone = result.phone
            self.nid = result.nid




    # @api.onchange('nid')
    # def based_on_nid(self):
    #     for f in self:
    #         return {'domain': {'visitor': [('nid', '=', f.nid)]}}

    visitor = fields.Many2one('visitor_log_book.visitor',string='Visitor Phone',required=True)
    visitor_id = fields.Char(string='Visitor ID',required=True)
    card_no = fields.Char(string='Card No')
    company = fields.Char(string='Company')
    designation = fields.Char(string='Designation')
    purpose = fields.Selection([('official','Official'),('personal','Personal')],default='official')
    nid = fields.Char(string='NID(National ID')
    vi_phone = fields.Char(string='Visitor Name',required=True)

    @api.onchange('desired_person')
    def based_on_desired_person(self):
        result = self.env['visitor_log_book.employee'].search([('id', '=', self.desired_person.id)])
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
            self.desired_person = result.id
            self.email = result.email
            self.department = result.department.name
            self.position = result.position.name
            self.employee_id = result.employee_id

    @api.onchange('email')
    def based_on_email(self):
        result = self.env['visitor_log_book.employee'].search([('email', '=', self.email)])
        if result:
            self.desired_person = result.id
            self.em_phone = result.phone
            self.department = result.department.name
            self.position = result.position.name
            self.employee_id = result.employee_id

    @api.onchange('employee_id')
    def based_on_employee_id(self):
        result = self.env['visitor_log_book.employee'].search([('employee_id', '=', self.employee_id)])
        if result:
            self.desired_person = result.id
            self.email = result.email
            self.department = result.department.name
            self.position = result.position.name
            self.em_phone = result.phone

    desired_person = fields.Many2one('visitor_log_book.employee', string='Name')#for purpose
    department = fields.Char(string='Department')
    position = fields.Char(string='Position')
    employee_id = fields.Char(string='Employee ID',required=True)
    em_phone = fields.Char(string='Phone',required=True) #for purpose
    email = fields.Char(string='Email',required=True)

    check_in = fields.Datetime(string='Checkin Time',required=True,default = fields.Datetime.now)
    check_out = fields.Datetime(string='Checkout Time')
    state = fields.Selection([('checkin','CheckIn'),('checkout','CheckOut')],readonly=True)
    is_checkout = fields.Boolean(string='Is Checkout',default=True)



    def checkout_btn(self):
        for f in self:
            f.state='checkout'
            f.check_out=datetime.now()
            try:
                #sending checkout msg to channel
                channel_id = self.env['mail.channel'].search([('name','=','authority')]) #channel name
                channel_id.message_post(
                    subject='Checkout',
                    body="Mr.{0} has CheckOut after meet  {1}".format(f.visitor.phone,f.desired_person.name),
                    subtype='mail.mt_comment')
            except:
                pass

    #Send CheckInMsg to channel
    def SendCheckInMsg(self,visitor,desired_person):
        try:
            channel_id = self.env['mail.channel'].search([('name', '=', 'authority')])  # channel name
            channel_id.message_post(
                subject='Checkout',
                body="Mr.{0} has Checkin to meet with  {1}".format(visitor,desired_person),
                subtype='mail.mt_comment')
            return
        except:
            pass


    @api.model
    def create(self, vals_list):
        result=super(CheckInOut, self).create(vals_list)
        if result['is_checkout']==True:
            result['state']='checkin'
            result['is_checkout']=False

            #for descuss notification
            visitor=result['visitor'].copy_data()
            visitor=visitor[0]['phone']
            desired_person=result['desired_person'].copy_data()
            desired_person=desired_person[0]['name']

            self.SendCheckInMsg(visitor, desired_person)

        return result







            
