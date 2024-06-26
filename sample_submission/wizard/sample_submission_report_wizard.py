from odoo import api, fields, models, tools, _


class SimpleSubmissionReportWizard(models.TransientModel):
    _name = 'sample.sub.generate.wiz'

    date = fields.Date('Date Of Submission')
    sample_submission_ids = fields.Many2many('sample.submission', string="Submission Records", required=True)
    is_invoiced_or_not = fields.Selection([
        ('invoiced', 'Invoiced'), ('all', 'All Records')
    ], string='Invoiced/All', default='invoiced')

    # function trigger when date or is_invoiced_or_not field is changed and fetch the appropriate records
    @api.onchange('date', 'is_invoiced_or_not')
    def _onchange_fetch_sample_submission_ids(self):
        for rec in self:
            if rec.date and rec.is_invoiced_or_not == 'invoiced':  # only fetch the invoiced submission records
                invoiced_submission_rec = self.env['sample.submission'].search([
                    ('date_of_submission', '=', rec.date), ('invoiced', '=', True)
                ])
                self.sample_submission_ids = [(6, 0, invoiced_submission_rec.ids)]
            elif rec.date and rec.is_invoiced_or_not == 'all':  # fetch all the submission records
                submission_rec = self.env['sample.submission'].search([
                    ('date_of_submission', '=', rec.date)
                ])
                self.sample_submission_ids = [(6, 0, submission_rec.ids)]

    def generate_simple_report_pdf(self):
        data = {
            'submission_ids': self.sample_submission_ids.ids,
        }
        return self.env.ref('sample_submission.action_sample_report_from_wizard').report_action([], data=data)

    def generate_simple_report_excel(self):
        data = {
            'submission_ids': self.sample_submission_ids.ids,
        }
        return self.env.ref('sample_submission.action_sample_sub_xlsx_reports').report_action([], data=data)
