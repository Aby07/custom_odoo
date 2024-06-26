from odoo import models, fields, api


class SubmissionMaterialWizard(models.TransientModel):
    _name = 'submission.material.wizard'
    _description = 'Material Wizard'

    sample_sub_id = fields.Many2one('sample.submission', string="Sample Submission")
    material_line_ids = fields.One2many('sample.sub.material.wizard.line', 'submission_wizard_id', string="Materials")

    def action_add_material(self):
        self.ensure_one()
        sample_submission = self.sample_sub_id
        line_list = []
        sample_submission.material_line_ids = [(5, 0, 0)]
        for line in self.material_line_ids:
            material_vals = {
                'material_id': line.material_id.id,
                'qty': line.qty,
                'remarks': line.remarks
            }
            line_list.append((0, 0, material_vals))
        sample_submission.write({'material_line_ids': line_list})


class SampleSubmissionMaterialWizardLine(models.TransientModel):
    _name = 'sample.sub.material.wizard.line'
    _description = 'Material Wizard Line'

    submission_wizard_id = fields.Many2one('submission.material.wizard', string="Wizard")
    material_id = fields.Many2one('product.product', string="Material")
    qty = fields.Float(string="Quantity")
    remarks = fields.Char(string="Remarks")
