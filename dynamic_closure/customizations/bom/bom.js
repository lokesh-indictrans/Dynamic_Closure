
frappe.ui.form.on("BOM", {
	refresh: function(frm) {
		frm.fields_dict['items'].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
			return {
				query: "dynamic_closure.customizations.bom.bom.get_items",
				filters: {'is_sales_item': 1}
			}
		}
	}
});