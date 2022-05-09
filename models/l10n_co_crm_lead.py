# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    companyName = fields.Char("Name of the Company")
    companyBrandName = fields.Char("Brand")
    x_name1 = fields.Char("Primer Nombre")
    x_name2 = fields.Char("Segundo Nombre")
    x_lastname1 = fields.Char("Primer Apellido")
    x_lastname2 = fields.Char("Segundo Apellido")
    xcity = fields.Many2one('res.country.state.city', "Municipality", default=lambda self: self.env.user.company_id.partner_id.xcity)
    is_company = fields.Boolean(string="Es compañia?")
    xidentification = fields.Char("Número de documento")
    pos_name = fields.Char("Point of Sales Name")
    xbirthday = fields.Date("Birthday")
    formatedNit = fields.Char(
		string='NIT Formatted',
		compute="_compute_concat_nit",
		store=True
	)
    dv = fields.Integer(string=None, compute="_compute_concat_nit", store=True)
    companyType = fields.Selection(related='company_type')
    company_type = fields.Selection(
		[
			('person', 'Individual'),
			('company', 'Company')
		], default="person"
	)
    doctype = fields.Selection(
		[
			("1", ("No identification")),
			("11", ("11 - Birth Certificate")),
			("12", ("12 - Identity Card")),
			("13", ("13 - Citizenship Card")),
			("21", ("21 - Alien Registration Card")),
			("22", ("22 - Foreigner ID")),
			("31", ("31 - TAX Number (NIT)")),
			("41", ("41 - Passport")),
			("42", ("42 - Foreign Identification Document")),
			("43", ("43 - No Foreign Identification")),

		], "Type of Identification", default="1"
	)
    personType = fields.Selection(
		[
			("1", "Natural"),
			("2", "Juridical")
		],
		"Type of Person",
		default="1"
	)

    @api.onchange('xcity')
    def _onchange_xcity(self):
        if self.xcity:
            if self.xcity.state_id:
                self.state_id = self.xcity.state_id.id
            if self.xcity.country_id:
                self.country_id = self.xcity.country_id.id
    
    def get_doctype(self):
        result = []
        for item in self.env['crm.lead'].fields_get(self)['doctype']['selection']:
            result.append({'id': item[0], 'name': item[1]})
            print(result,"RESULT1")
            return result    

    def get_persontype(self):
        result = []
        for item in self.env['crm.lead'].fields_get(self)['personType']['selection']:
            result.append({'id': item[0], 'name': item[1]})
            print(result,"RESULT2")
            return result
    
    @api.depends('xidentification')
    def _compute_concat_nit(self):
        for partner in self:
            _logger.info("-"*500)
            _logger.info(partner.doctype)
            if partner.doctype == "31":
                self._check_ident()
                self._check_ident_num()
                if partner.xidentification == False:
                    partner.xidentification = ''
                else:
                    partner.formatedNit = ''
                    
                    s = str(partner.xidentification)[::-1]
                    newnit = ''.join(s[i:i+3] for i in range(0, len(s), 3))
                    newnit = newnit[::-1]
                    
                    nitList = [
						newnit,
						# Calling the NIT Function
						# which creates the Verification Code:
						self._check_dv(str(partner.xidentification))
					]
                    
                    formatedNitList = []
                    
                    for item in nitList:
                        if item is not '':
                            formatedNitList.append(item)
                            partner.formatedNit = '-' .join(formatedNitList)
                            
                    partner.dv = nitList[1]
