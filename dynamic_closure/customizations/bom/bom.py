from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.controllers.item_variant import create_variant
from six import string_types
import json


@frappe.whitelist()
def get_items(doctype, txt, searchfield, start, page_len, filters, as_dict):
	return frappe.db.sql(""" 
		select 
			name 
		from 
			`tabItem` 
		where 
			is_sales_item = 1 
			and has_variants < 2
			and name like '{txt}' """.format(txt= "%%%s%%" % txt))

@frappe.whitelist()
def get_boms(item):
	bom = frappe.get_value("BOM",{"item":item,"is_default":1,"is_active":1},["name","bom_level"],as_dict=1)
	if bom:
		return bom

@frappe.whitelist()
def get_attribute_value(doctype, txt, searchfield, start, page_len, filters, as_dict):
	return frappe.db.sql(""" 
		select 
			name 
		from 
			`tabItem Attribute Value` 
		where 
			parent = '{parent}'
			and name like '{txt}' """.format(parent= filters.get('attribute'),txt= "%%%s%%" % txt))