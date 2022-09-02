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
		if(row.item_code && row.qty)
		{
			frappe.call({
					method: 'dynamic_closure.customizations.quotation.quotation.get_attributes',
					args: {
						"item": row.item_code
		            },
					callback: (r) => {
						var	fields = []
						if(r.message)
						{
							$.each(r.message, function(i, v) {
								var dic = {
									"label": __(v.item_code),
									"fieldname": v.item_code.split(' ').join('_').toLowerCase(),
									"fieldtype": "Link",
									"options": "Item Attribute Value",
									"reqd": 1,
									get_query:function() {
										return {
											"filters": {
												"parent": ["=",v.attribute]
											}
										}
									},
								}
								fields.push(dic)
							
							});
							var dialog = new frappe.ui.Dialog({
							title: __('Attributes'),
							keep_open: true,
							fields: fields,
							onhide: () => {
								}
							});
							dialog.set_primary_action(__('Submit'), () => {
								frm.save()
								create_cpq(frm,row,dialog,cdt,cdn);
							});
							dialog.show();


						}
					}
				});
		}
		else
		{
			frappe.msgprint("Please enter item and quantity")
		}
	},
	qty: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		if(row.item_code && row.qty)
		{
			frappe.call({
					method: 'dynamic_closure.customizations.quotation.quotation.get_attributes',
					args: {
						"item": row.item_code
		            },
					callback: (r) => {
						var	fields = []
						if(r.message)
						{
							$.each(r.message, function(i, v) {
								var dic = {
									"label": __(v.item_code),
									"fieldname": v.item_code.split(' ').join('_').toLowerCase(),
									"fieldtype": "Link",
									"options": "Item Attribute Value",
									"reqd": 1,
									get_query:function() {
										return {
											"filters": {
												"parent": ["=",v.attribute]
											}
										}
									},
								}
								fields.push(dic)
							
							});
							var dialog = new frappe.ui.Dialog({
							title: __('Attributes'),
							keep_open: true,
							fields: fields,
							onhide: () => {
								}
							});
							dialog.set_primary_action(__('Submit'), () => {
								frm.save()
								create_cpq(frm,row,dialog,cdt,cdn);
							});
							dialog.show();


						}
					}
				});
		}
		else
		{
			frappe.msgprint("Please enter item and quantity")
		}
	}
});


var create_cpq = function(frm,row,dialog,cdt,cdn){
	frappe.call({
				method: 'dynamic_closure.customizations.quotation.quotation.create_cpq',
				async: false,
				args: {
					"item": row.item_code,
					"item_name": row.item_name,
					"uom": row.uom,
	                "data": dialog.get_values(),
	                "doc": frm.doc,
	                "qty": row.qty
	            },
				callback: (r) => {
					if(r.message)
					{
						frappe.model.set_value(cdt, cdn, "rate", r.message.total_cost)
						frappe.msgprint("Quotation Item CPQ created successfully")
					}
				}
			});
};
