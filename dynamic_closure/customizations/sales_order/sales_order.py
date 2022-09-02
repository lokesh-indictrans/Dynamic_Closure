from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.controllers.item_variant import create_variant
from six import string_types
import json
from frappe.utils import flt
from erpnext.controllers.item_variant import get_variant,create_variant

def validate(doc, method=None):
	for row in doc.items:
		qic = frappe.get_value("Quotation Item CPQ",{"item":row.item_code,"quotation":row.prevdoc_docname},"name")

		if qic:
			qic_doc = frappe.get_doc("Quotation Item CPQ",qic)
			for itm in qic_doc.items:
				if itm.get('item_attribute'):
					args = {frappe.get_value("Item Attribute Value",itm.get('item_attribute'),"parent"):itm.get('item_attribute')}
					if not get_variant(itm.get('item_code'),args):
						variant = create_variant(itm.get('item_code'),args)
						variant.save()

def on_submit(doc, method=None):
	for row in doc.items:

		qic = frappe.get_value("Quotation Item CPQ",{"item":row.item_code,"quotation":row.prevdoc_docname},"name")

		if qic:
			qic_doc = frappe.get_doc("Quotation Item CPQ",qic)
			bom_doc = frappe.new_doc("BOM")
			bom_doc.selling_price_list = qic_doc.price_list
			bom_doc.currency = qic_doc.currency
			bom_doc.item = qic_doc.item
			bom_doc.item_name = qic_doc.item_name
			bom_doc.uom = qic_doc.item_uom
			bom_doc.quantity = row.get('qty')
			bom_doc.operations = qic_doc.operations
			bom_doc.items = qic_doc.items


			for itm in bom_doc.items:
				if itm.get('item_attribute'):
					args = {frappe.get_value("Item Attribute Value",itm.get('item_attribute'),"parent"):itm.get('item_attribute')}
					variant = get_variant(itm.get('item_code'),args)
					itm.update({"item_code":variant,"item_name":variant})
			bom_doc.flags.ignore_permissions = True
			bom_doc.save()
			# bom_doc.submit()


				
