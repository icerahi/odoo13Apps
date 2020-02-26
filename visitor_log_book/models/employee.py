
from odoo import fields,models,api,_

class Department(models.Model):
    _name = 'employee.department'
    name = fields.Char(string="Name ")

class Position(models.Model):
    _name = 'employee.position'
    name = fields.Char(string='Name')

class Employee(models.Model):
    _name = 'visitor_log_book.employee'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name',required=True) #for purpose we change string label name
    department = fields.Many2one('employee.department',string='Department')
    position = fields.Many2one('employee.position',string='Position')
    image = fields.Binary(string='Image')
    phone = fields.Char(string='Phone',required=True) # for purpose we change string as name
    email = fields.Char(string='Email',required=True)
    employee_id = fields.Char(string='employee ID',required=True,copy=False,index=True,default=lambda self:_('New'))

    total_guest = fields.Integer(string='Total Visites',compute='get_total')

    def get_total(self):
        count=self.env['visitor_log_book.checkinout'].search_count([('desired_person','=',self.id)])
        self.total_guest=count



    def get_total_guest(self):
        return {
            'name': 'All Guests',
            'res_model': 'visitor_log_book.checkinout',
            'domain': [('desired_person', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }



    @api.model
    def create(self, vals_list):
        if vals_list.get('employee_id',_('New')) == 'New':
            vals_list['employee_id']=self.env['ir.sequence'].next_by_code('employee_id.sequence') or _('New')
        result=super(Employee, self).create(vals_list)
        return result


    # @api.constrains('phone')
    # def check_phone_validation(self):
    #     result = self.env['visitor_log_book.employee'].search([('phone', '=', self.phone)])
    #     if len(result)>1:
    #         raise Warning('This Phone Number Already Register in our record book!')
    #

