from odoo import models, fields, api


class SampleSubmissionListView(models.Model):
    _name = 'sample.submission.list.view'
    _description = 'Sample Submission List View'

    sequence_number = fields.Char('Sequence Number')
    date = fields.Date('Date')
    amount = fields.Float('Amount')
    price = fields.Float('Price')
    invoice_status = fields.Boolean( string='Invoice Status')
    collected_payment = fields.Float('Collected Payment')
    balance = fields.Float('Balance')
    total = fields.Float('Total')
    product_qty = fields.Float('Product Qty', compute='_compute_product_qty')
    sum_of_cost = fields.Float('Sum of Cost', compute='_compute_sum_of_cost')
    profit = fields.Float('Profit', compute='_compute_profit')
    sample_sub_id = fields.Many2one('sample.submission')

    @api.depends('amount', 'price', 'collected_payment')
    def _compute_balance(self):
        for record in self:
            record.balance = record.amount - record.collected_payment

    @api.depends('amount', 'price', 'collected_payment')
    def _compute_total(self):
        for record in self:
            record.total = record.amount + record.price - record.collected_payment

    @api.depends('product_qty')
    def _compute_product_qty(self):
        for record in self:
            record.product_qty = record.product_qty

    @api.depends('amount', 'price')
    def _compute_sum_of_cost(self):
        for record in self:
            record.sum_of_cost = record.amount * record.price

    @api.depends('amount', 'price', 'collected_payment')
    def _compute_profit(self):
        for record in self:
            record.profit = record.amount - (record.amount * record.price)



