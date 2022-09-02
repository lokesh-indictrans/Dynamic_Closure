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
	attribute_val = ""
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
			if row.get('bom'):
				bom2 = frappe.get_doc("BOM",row.get('bom'))
				cpq_doc.items.extend(bom2.get('items'))
		
		for row in cpq_doc.items:
			for itm in data.keys():
				if itm.replace("_", " ").title() == bom_doc.attribute:
					attribute_val = data.get(itm)
				if itm.replace("_", " ").title() == row.get('item_code'):
					row.item_attribute = data.get(itm)
					row.rate = frappe.get_value("Item Attribute Value",data.get(itm),"price")
			tag = frappe.get_value("Item",row.get('item_code'),"_user_tags")
			if tag:
				row.item_attribute = tag.replace(",","")

			if bom_doc.is_multiple_items:
				if row.get('related_attribute_value') and row.get('related_attribute_value') != attribute_val and row not in remove_items:
					remove_items.append(row)

			if not row.rate:
				row.rate = frappe.get_value("Item Price",{"price_list":doc.get('selling_price_list'),"item_name":row.get("item_code")},"price_list_rate")
			row.amount = flt(row.rate*row.qty,2)
			total_cost += flt(row.amount,2)

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

@frappe.whitelist()
def get_attributes(item):
	bom = frappe.get_value("BOM",{"item":item,"is_default":1,"is_active":1},["name","bom_level"],as_dict=1)
	
	remove_items,unique_items,boms = [],[],[]
	boms.append(bom.get('name'))

	if bom.get('bom_level') > 0:
		bom_lst = frappe.db.sql("select bom from `tabBOM Item` where parent = '{0}' and bom is not null".format(bom.get('name')),as_dict=1,debug=0)
		bom_lst = [row.get('bom') for row in bom_lst]
		if bom_lst:
			boms.extend(bom_lst)

	bom_tuple = "(" + ",".join([ "'{0}'".format(row) for row in \
		boms ]) + ")"


	get_templates = frappe.db.sql(""" 
		select 
			distinct(boi.item_code),iva.attribute
		from
			`tabBOM Item` as boi, `tabItem` as itm, `tabItem Variant Attribute` as iva
		where
			boi.item_code = itm.name 
			and iva.parent = itm.name
			and boi.parent in {0}
			and itm.has_variants = 1

			 """.format(bom_tuple),as_dict=1,debug=1)

	items = "(" + ",".join([ "'{0}'".format(row.get('item_code')) for row in \
		get_templates ]) + ")"

	get_tagged_items = frappe.db.sql(""" 
		select 
			name 
		from 
			tabItem 
		where 
			_user_tags is not null and 
			name in {0} """.format(items),as_dict=1,debug=0)

	tagged_items_list = [row.get('name') for row in get_tagged_items]


	for row in get_templates:
		if row.get('item_code') in unique_items and row not in remove_items:
			remove_items.append(row)
		else:
			unique_items.append(row.get('item_code'))
		if row.get("item_code") in tagged_items_list and row not in remove_items:
			remove_items.append(row)

	for row in remove_items:
		get_templates.remove(row)

	return get_templates