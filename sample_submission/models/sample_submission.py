from odoo import models, fields, _, api
from odoo.exceptions import ValidationError, UserError


class SampleSubmission(models.Model):
    _name = 'sample.submission'
    _description = 'Sample Submission Model'
    _rec_name = 'sl_no'

    sl_no = fields.Char(string='Sample Sequence Number', required=True, copy=False, readonly=True,
                        default=lambda self: _('New'))
    name = fields.Char(string='Name of Sample', required=True)
    customer = fields.Many2one('res.partner', 'Customer')
    date_of_submission = fields.Date(string='Date of Submission')
    description = fields.Text(string='Description')
    price = fields.Float(string='Price')
    discount = fields.Float(string='Discount')
    vat = fields.Many2many('account.tax', string='VAT')
    stage = fields.Selection([
        ('pending', 'Pending'),
        ('doing', 'Doing'),
        ('completed', 'Completed')
    ], string='Stage', default='pending')
    material_line_ids = fields.One2many('sample.submission.material.line', 'submission_id', string='Materials Required')
    invoiced = fields.Boolean(string='Invoiced', readonly=True, default=False)
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    list_view_ids = fields.One2many('sample.submission.list.view', 'sample_sub_id', string='List View')

    # To Doing Button Action
    def action_to_doing(self):
        self.stage = 'doing'

    # Completed Buttton Action
    def action_completed(self):
        self.stage = 'completed'

    # Print PDF Report Action
    def action_generate_pdf_report(self):
        data = {
            'rec_id': self.id
        }
        report = self.env.ref('sample_submission.action_sample_submit_report').report_action([], data=data)
        return report

    # Print Excel Report Action
    def action_generate_xlsx_report(self):
        data = {
            'rec_id': self.id
        }
        report = self.env.ref('sample_submission.action_sample_submit_xlsx_report').report_action([], data=data)
        return report

    # show a warning message for confirm the user for create the invoice on account.move
    def action_generate_invoice(self):
        self.ensure_one()
        view_id = self.env.ref("sample_submission.view_create_invoice_wiz_form").id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'confirm.create.invoice.wiz',
            'view_id': view_id,
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sample_sub_id': self.id,
            },
        }

    # Show created invoice of current simple submission record
    def action_view_invoice(self):
        self.ensure_one()
        if self.invoiced:
            res_model = 'account.move'
            return {
                'type': 'ir.actions.act_window',
                'name': 'Simple Submission Invoice',
                'view_mode': 'form',
                'res_model': res_model,
                'res_id': self.invoice_id.id,
                'context': "{'create': False}"
            }

    # trigger the wizard action, which show the wizard for creation and modification of material on material_line_ids
    def action_add_product_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'submission.material.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sample_sub_id': self.id,
                'default_material_line_ids': [(0, 0, {
                    'material_id': line.material_id.id,
                    'qty': line.qty,
                    'remarks': line.remarks,
                }) for line in self.material_line_ids],
            },
        }

    # create record in sample.submission.list.view model
    def create_list_rec(self, vals):
        list_view_obj = self.env['sample.submission.list.view']
        list_view_vals = {
            'sequence_number': vals.get('sl_no', ),
            'date': vals.get('date_of_submission'),
            'price': vals.get('price', 0.0),
            'invoice_status': vals.get('invoiced'),
            'collected_payment': vals.get('collected_payment', 0.0),
            'balance': vals.get('amount', 0.0) - vals.get('collected_payment', 0.0),
            'total': vals.get('amount', 0.0) + vals.get('price', 0.0) - vals.get('collected_payment', 0.0),
            'product_qty': vals.get('product_qty', 0.0),
            'sum_of_cost': vals.get('amount', 0.0) * vals.get('price', 0.0),
            'profit': vals.get('amount', 0.0) - (vals.get('amount', 0.0) * vals.get('price', 0.0)),
        }
        list_view_obj.create(list_view_vals)

    @api.model
    def create(self, vals):
        if vals.get('sl_no', _('New')) == _('New'):
            vals['sl_no'] = self.env['ir.sequence'].next_by_code('sample.submission') or _('New')
        res = super(SampleSubmission, self).create(vals)
        res.create_list_rec(vals)  # call function for create record in sample.submission.list.view
        return res


class SampleSubmissionLine(models.Model):
    _name = 'sample.submission.material.line'

    submission_id = fields.Many2one('sample.submission', string='Sample Submission', required=True, ondelete='cascade')
    sl_no = fields.Integer('Sl.No')
    material_id = fields.Many2one('product.product', string='Material', required=True)
    qty = fields.Float(string='Quantity', required=True)
    remarks = fields.Char(string='Remarks')
