from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    sample_submission_id = fields.Many2one('sample.submission', string='Sample Submission', readonly=True)
