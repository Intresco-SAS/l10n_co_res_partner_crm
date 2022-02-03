# -*- coding: utf-8 -*-
{
    'name': 'Terceros - Colombia (CRM)',
    'category': 'Localization',
    'version': '12.0',
    'summary': 'Terceros Colombia: Extendido de Partner / '
               'Modulo de CRM - Odoo 12.0',
    'depends': [
        'l10n_co_res_partner', 'crm',
    ],
    'data': [
        'views/crm_lead_view.xml',
        'views/template_quantation.xml',
        'views/template_invoice.xml'
    ],
}
