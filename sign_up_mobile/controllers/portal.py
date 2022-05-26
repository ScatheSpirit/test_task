# -*- coding: utf-8 -*-

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalMobile(CustomerPortal):

    # Add 'mobile' field to optional billing fields use in details_form_validate
    # to edit mobile from portal.portal_my_details
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name", "mobile"]
