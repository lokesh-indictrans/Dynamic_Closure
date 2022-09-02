
frappe.ui.form.on("BOM", {
	validate: function(frm) {
		if(frm.doc.items && frm.doc.uom == "Inch")
		{
			$.each(frm.doc.items, function(i, v) {
				frappe.model.set_value(v.doctype, v.name, "uom", "Feet");
				if(!v.pieces)
				{
					v.pieces = 1;
				}
				var qty = v.pieces*frm.doc.quantity/12;
				frappe.model.set_value(v.doctype, v.name, "qty", qty)
			})
		}
	},
	refresh: function(frm) {
		frm.fields_dict['items'].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
			return {
				query: "dynamic_closure.customizations.bom.bom.get_items",
				filters: {'is_sales_item': 1}
			}
		}
		frm.fields_dict['items'].grid.get_field("related_attribute_value").get_query = function(doc, cdt, cdn) {
			return {
				query: "dynamic_closure.customizations.bom.bom.get_attribute_value",
				filters: {'attribute': frm.doc.attribute}
			}
		}
	}
});

frappe.ui.form.on("BOM Item", {
	item_code: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		if(row.item_code)
		{
			if(frm.doc.uom == "Inch")
			{
				if(!row.pieces)
				{
					row.pieces = 1;
				}
				var qty = row.pieces*frm.doc.quantity/12;
				frappe.model.set_value(cdt, cdn, "uom", "Feet")
				frappe.model.set_value(cdt, cdn, "qty", qty)
			}
			frappe.call({
				method: "dynamic_closure.customizations.bom.bom.get_boms",
				args:{
					"item": row.item_code
				},
				callback: (r) => {
					if(r.message)
					{
						frm.set_value("bom_level",r.message.bom_level + 1);
						frappe.model.set_value(cdt, cdn, "bom", r.message.name)
					}
					else
					{
						frm.set_value("bom_level",0);
					}

				}
			});
		}
	}
});