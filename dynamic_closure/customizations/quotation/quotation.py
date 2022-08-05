from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.controllers.item_variant import create_variant
from six import string_types
import json
from frappe.utils import flt

def validate(doc, method=None):
	pass

@frappe.whitelist()
def create_cpq(item,item_name,uom,data,doc):
	data = json.loads(data)
	doc = json.loads(doc)
	cpq_doc = frappe.new_doc("Quotation Item CPQ")
	cpq_doc.item = item
	bom = frappe.get_value("BOM",{"item":item},"name")
	remove_items,unique_items = [],[]

	total_cost = 0
	if bom:
		bom_doc = frappe.get_doc("BOM",bom)
		cpq_doc.price_list = doc.get('selling_price_list')
		cpq_doc.currency = doc.get('currency')
		cpq_doc.item_name = item_name
		cpq_doc.item_uom = uom
		cpq_doc.operations = bom_doc.get('operations')
		cpq_doc.items = bom_doc.get('items')
		cpq_doc.quotation = doc.get('name')
		
		for row in cpq_doc.items:
			if row.get('item_code') in unique_items:
				remove_items.append(row)
			else:
				unique_items.append(row.get('item_code'))
			if data.get('screen_size') == "Screen Size 13" and "15" in row.get('item_code'):
				remove_items.append(row)
			elif data.get('screen_size') == "Screen Size 15" and "13" in row.get('item_code'):
				remove_items.append(row)

			if row.get('item_code') == "Chipset and Processor":
				row.item_attribute = data.get('chipset_and_processor_val')
			elif row.get('item_code') == "RAM":
				row.item_attribute = data.get('ram')
			elif row.get('item_code') == "SDD":
				row.item_attribute = data.get('sdd')
			elif row.get('item_code') == "Screen Size":
				row.item_attribute = data.get('screen_size')
			elif row.get('item_code') in ["Laptop Chassis- 13 Inch" or "Laptop Chassis- 15 Inch"]:
				row.item_attribute = data.get('chassis_width')

			row.rate = frappe.get_value("Item Price",{"price_list":doc.get('selling_price_list'),"item_name":row.get("item_code")},"price_list_rate")

			total_cost += flt(row.rate)

		for row in remove_items:
			cpq_doc.items.remove(row)

		cpq_doc.flags.ignore_permissions = True
		cpq_doc.operating_cost = bom_doc.operating_cost
		cpq_doc.total_cost = flt(total_cost + bom_doc.operating_cost,2)
		cpq_doc.save()

		return {"total_cost":cpq_doc.total_cost}
	
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