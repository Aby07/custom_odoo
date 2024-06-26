from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ConfirmCreateInvoiceWiz(models.TransientModel):
    _name = 'confirm.create.invoice.wiz'
    _description = 'Confirm Create Invoice Wizard'

    sample_sub_id = fields.Many2one('sample.submission', string="Sample Submission", readonly=True)
    warning_message = fields.Text('Warning', default="Are You Sure Want To Create Invoice..?", readonly=True)

    # Create the invoice record and post in the invoicing module if sample_sub_id found
    def action_create_invoice(self):
        self.ensure_one()
        sample_sub_id = self.sample_sub_id

        if not sample_sub_id:
            raise ValidationError("No sample submission selected.")

        for rec in sample_sub_id:
            lines = [(5, 0)]
            for line in rec.material_line_ids:
                line_vals = {
                    'product_id': line.material_id.id,
                    'quantity': line.qty,
                }
                lines.append((0, 0, line_vals))

            vals = {
                'move_type': 'out_invoice',
                'partner_id': rec.customer.id,
                'payment_reference': rec.description,
                'invoice_date': rec.date_of_submission,
                'invoice_line_ids': lines
            }
            invoice = self.env['account.move'].create(vals)  # create record in account.move

            if invoice:
                invoice.action_post()  # Post the invoice
                sample_sub_id.write({
                    'invoiced': True,
                    'invoice_id': invoice.id
                })  # Mark record as invoiced and link to invoice
                invoice.write({'sample_submission_id': sample_sub_id.id})  # Write sample_submission_id in account.move

            return {'type': 'ir.actions.act_window_close'}

    # cancel function on wizard cancel button
    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
