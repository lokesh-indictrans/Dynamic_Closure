from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.controllers.item_variant import create_variant
from six import string_types
import json

def validate(doc, method=None):
	pass


@frappe.whitelist()
def publish_tags(item_attribute,tagname):
	tag_doc = frappe.new_doc("Tag")
	tag_doc.__newname = tagname
	tag_doc.description = item_attribute + " " + tagname
	tag_doc.flags.ignore_permissions = True
	tag_doc.save()
	return True

@frappe.whitelist()
def publish_all_tags(item_attribute):
	tag_doc = frappe.new_doc("Tag")
	tag_doc.__newname = "ALL-" + item_attribute
	tag_doc.description = "ALL-" + item_attribute
	tag_doc.flags.ignore_permissions = True
	tag_doc.save()

	frappe.db.commit()
	return True
