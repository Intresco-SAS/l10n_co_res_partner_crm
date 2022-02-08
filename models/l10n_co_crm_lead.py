# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    x_name1 = fields.Char("Primer Nombre")
    x_name2 = fields.Char("Segundo Nombre")
    x_lastname1 = fields.Char("Primer Apellido")
    x_lastname2 = fields.Char("Segundo Apellido")
    xcity = fields.Many2one('res.country.state.city', "Municipality", default=lambda self: self.env.user.company_id.partner_id.xcity)

    @api.onchange('xcity')
    def _onchange_xcity(self):
        if self.xcity:
            if self.xcity.state_id:
                self.state_id = self.xcity.state_id.id
            if self.xcity.country_id:
                self.country_id = self.xcity.country_id.id
