from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class SimpleSubmissionReport(models.AbstractModel):
    _name = 'report.sample_submission.sample_submission_pdf_report'

    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        recid = data['rec_id']
        dat = self.get_sample_submission_data(recid)
        data.update(dat)
        return data

    def get_sample_submission_data(self, recid):
        sample_submission_record = self.env['sample.submission'].browse([recid])

        if sample_submission_record:
            return {
                'docs': sample_submission_record,
            }
        else:
            raise UserError('no data found ')
