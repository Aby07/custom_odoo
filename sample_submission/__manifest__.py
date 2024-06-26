# -*- coding: utf-8 -*-
{
    'name': 'Sample Submission',
    'version': '16.0',
    'summary': 'Manage Sample Submissions and generate invoices',
    'sequence': -1,
    'description': """Sample Submission App""",
    'category': 'Sample Submission Demo',
    'depends': ['base', 'stock'],
    'data': [
        'data/sample_submission_data.xml',
        'security/ir.model.access.csv',
        'security/sample_submission_security.xml',
        'wizard/submission_line_material_wizard.xml',
        'wizard/confirm_create_invoice_wizard_view.xml',
        'wizard/sample_submission_report_wizard_view.xml',
        'reports/sample_submission_report.xml',
        'reports/sample_submission_report_template.xml',
        'reports/sample_submission_report_wizard.xml',
        'reports/sample_submission_report_wizard_template.xml',
        'views/sample_submission_view.xml',
        'views/account_move_view.xml',
        'views/sample_submission_list_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}