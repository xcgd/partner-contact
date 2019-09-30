# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    group_id = fields.Many2one(
        comodel_name='res.partner',
        string='Group',
        domain=[("is_group", "=", True)],
    )

    is_group = fields.Boolean(
        string="Is a Group",
        default=False,
    )

    @api.model
    def _commercial_fields(self):
        res = super()._commercial_fields()
        res.append('group_id')
        return res
