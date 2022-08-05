from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.controllers.item_variant import create_variant
from six import string_types
import json


@frappe.whitelist()
def get_items(doctype, txt, searchfield, start, page_len, filters, as_dict):
	print(">>>>>>>>>>>>>>>>>>>>>>>>.customizations")
	return frappe.db.sql(""" 
		select 
			name 
		from 
			`tabItem` 
		where 
			is_sales_item = 1 
			and has_variants < 2
			and name like '{txt}' """.format(txt= "%%%s%%" % txt))