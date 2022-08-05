frappe.ui.form.on('Quotation', {
	refresh: function(frm) {
		frm.fields_dict['items'].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
			return {
				query: "dynamic_closure.customizations.quotation.quotation.get_items",
				filters: {'is_sales_item': 1}
			}
		}
	}
});

frappe.ui.form.on('Quotation Item', {
	item_code: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		if(row.item_code)
		{
			var dialog = new frappe.ui.Dialog({
				title: __('Attributes'),
				keep_open: true,
				fields: [
					{
						"label": __(""),
						"fieldname": "section_break1",
						"fieldtype": "Section Break"
					},
					{
						"label": __("RAM"),
						"fieldname": "ram",
						"fieldtype": "Link",
						"options": "Item Attribute Value",
						"reqd": 1,
						get_query:function() {
							return {
								"filters": {
									"parent": ["=","Memory Storage"]
								}
							}
						},
					},
					{
						"label": __("SDD"),
						"fieldname": "sdd",
						"fieldtype": "Link",
						"options": "Item Attribute Value",
						"reqd": 1,
						get_query:function() {
							return {
								"filters": {
									"parent": ["=","Disk Storage"]
								}
							}
						}
					},
					{
						"label": __("Screen Size"),
						"fieldname": "screen_size",
						"fieldtype": "Link",
						"options": "Item Attribute Value",
						"reqd": 1,
						get_query:function() {
							return {
								"filters": {
									"parent": ["=","Screen Size"]
								}
							}
						}
					},
					{
						"label": __(""),
						"fieldname": "column_break_1",
						"fieldtype": "Column Break"
					},
					{
						"label": __("Chipset and Processor Value"),
						"fieldname": "chipset_and_processor_val",
						"fieldtype": "Link",
						"options": "Item Attribute Value",
						"reqd": 1,
						get_query:function() {
							return {
								"filters": {
									"parent": ["in","Apple, Intel"]
								}
							}
						},
					},
					{
						"label": __("Chassis Width"),
						"fieldname": "chassis_width",
						"fieldtype": "Link",
						"options": "Item Attribute Value",
						"reqd": 1,
						get_query:function() {
							return {
								"filters": {
									"parent": ["=", "Width"]
								}
							}
						},
					},
					{
						"label": __("Chassis Depth"),
						"fieldname": "chassis_depth",
						"fieldtype": "Link",
						"options": "Item Attribute Value",
						"reqd": 1,
						get_query:function() {
							return {
								"filters": {
									"parent": ["=", "Depth"]
								}
							}
						},
					},
				],
			onhide: () => {
					
				}
			});

			dialog.set_primary_action(__('Submit'), () => {
				frm.save()
				frappe.call({
					method: 'dynamic_closure.customizations.quotation.quotation.create_cpq',
					async: false,
					args: {
						"item": row.item_code,
						"item_name": row.item_name,
						"uom": row.uom,
		                "data": dialog.get_values(),
		                "doc": frm.doc
		            },
					callback: (r) => {
						if(r.message)
						{
							console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..",r.message)
							frappe.model.set_value(cdt, cdn, "rate", r.message.total_cost)
							frappe.msgprint("Quotation Item CPQ created successfully")
						}
					}
				});

			});

			dialog.show();
		}
	}
});

// cur_frm.fields_dict['items'].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
// 		return {
// 				"query": "dynamic_closure.customizations.quotation.quotation.get_items"
// 		}

// frm.fields_dict['items'].grid.get_field('expense_account').get_query = function(doc) {
// 			if (erpnext.is_perpetual_inventory_enabled(doc.company)) {
// 				return {
// 					query: "dynamic_closure.customizations.quotation.quotation.get_items"
// 				}
// 			}
// 		}