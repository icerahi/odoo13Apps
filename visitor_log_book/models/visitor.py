from odoo import models, fields, api, _, exceptions


class Designation(models.Model):
    _name = 'visitor.designation'
    name = fields.Char(string="Name ")

class Company(models.Model):
    _name = 'visitor.company'

    name = fields.Char(string='Name')

class Visitor(models.Model):
    _name = 'visitor_log_book.visitor'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char('Visitor Phone',required=True)
    phone = fields.Char(string='Visitor Name',required=True)
    company = fields.Many2one('visitor.company')
    designation = fields.Many2one('visitor.designation')
    nid = fields.Char(string='NID(National ID)')
    visitor_id = fields.Char(string='Visitor ID',required=True,copy=False,index=True,default=lambda self:_('New'))
    total_visit = fields.Integer(string='Total Visites',compute='get_total_count')

    def get_total_count(self):
        count=self.env['visitor_log_book.checkinout'].search_count([('visitor','=',self.id)])
        self.total_visit=count



    def get_total_visit(self):
        return {
            'name': 'All Visits',
            'res_model': 'visitor_log_book.checkinout',
            'domain': [('visitor', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }


    def redirect_checkin(self):
        return {
            'name':'Visitor CheckIn',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'visitor_log_book.checkinout',

            #passing default value for the form
            'context':{'default_visitor':self.id},
            'target':'new',
        }

    @api.model
    def create(self, vals_list):
        if vals_list.get('visitor_id',_('New')) == 'New':
            vals_list['visitor_id']=self.env['ir.sequence'].next_by_code('visitor_id.sequence') or _('New')
        result=super(Visitor, self).create(vals_list)
        return result


    # @api.constrains('phone')
    # def check_phone_validation(self):
    #     result = self.env['visitor_log_book.employee'].search([('phone', '=', self.phone)])
    #     if len(result)>1:
    #         raise Warning('This Phone Number Already Register in our record book!')
    #
