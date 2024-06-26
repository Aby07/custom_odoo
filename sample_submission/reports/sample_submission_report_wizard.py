from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class SimpleSubmissionReport(models.AbstractModel):
    _name = 'report.sample_submission.sample_sub_pdf_report_from_wiz'

    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        sub_ids = data['submission_ids']
        submission_ids = self.env['sample.submission'].search([('id', 'in', sub_ids)])
        print('submission_ids', submission_ids)
        dat = self.get_sample_submission_data(submission_ids)
        data.update(dat)
        return data

    def get_sample_submission_data(self, submission_ids):

        if submission_ids:
            return {
                'docs': submission_ids,
            }
        else:
            raise UserError('no data found ')
