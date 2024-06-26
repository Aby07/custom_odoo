import xlsxwriter

from odoo import models


class SampleSubmitReportXlsx(models.AbstractModel):
    _name = 'report.sample_submission.sample_sub_xlsx_report_from_wiz'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sub_ids = data['submission_ids']
        submission_ids = self.env['sample.submission'].search([('id', 'in', sub_ids)])

        worksheet = workbook.add_worksheet('SAMPLE SUBMIT EXCEL REPORT')
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#DCE6F1',
            'border': 1
        })
        data_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yy',
            'align': 'center',
            'border': 1,
            'border_color': 'black'
        })
        worksheet.set_column('A:E', 30)

        headers = [
            'DATE',
            'CUSTOMER',
            'NAME',
            'PRICE',
        ]

        title = 'SAMPLE SUBMIT EXCEL REPORT'
        worksheet.merge_range('A1:D2', title, header_format)

        for col, header in enumerate(headers):
            worksheet.write(2, col, header, header_format)
        row = 3

        for record in submission_ids:
            worksheet.write(row, 0, record.date_of_submission, date_format)
            worksheet.write(row, 1, record.customer.name, data_format)
            worksheet.write(row, 2, record.name, date_format)
            worksheet.write(row, 3, record.price, data_format)
            row += 1
        workbook.close()


