# Copyright 2014 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2015 Antonio Espinosa <antonioea@antiun.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    job_position_id = fields.Many2one(
        comodel_name="res.partner.job_position",
        string="Categorized job position",
        help="Type of job position occupied by the contact in the company.",
    )

    @api.model
    def fields_get(self, allfields=None, attributes=None):

        res = super(ResPartner, self).fields_get(
            allfields=allfields, attributes=attributes
        )

        modification_data = {
            "job_position_id": {
                "string": _("Job Position"),
                "help": _(
                    "Type of job position occupied by the contact in the "
                    "company."
                ),
            }
        }

        for key, modification in modification_data.items():
            if key in res:
                dct = res[key].copy()
                dct.update(modification)
                res[key] = dct

        return res


class ResPartnerJobPosition(models.Model):
    """Manage the job position.

    The field "Job position" is used to reference the type of position held
    in the company in which works an individual type of partner.
    """

    _name = "res.partner.job_position"
    _description = "Job position"

    _order = "active desc, name"

    name = fields.Char(string="Wording", required=True, translate=True)

    code = fields.Char(string="Code", help="Unique code.", required=True)

    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ("unique_code", "UNIQUE(code)", "The code must be unique.")
    ]

    def name_get(self):
        """Returns the internal code concatenated with the wording"""
        return [
            (record.id, "%s - %s" % (record.code, record.name))
            for record in self
        ]
