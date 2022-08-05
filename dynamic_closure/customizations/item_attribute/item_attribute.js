frappe.ui.form.on('Item Attribute', {
	refresh: function(frm) {
		frm.fields_dict.item_attribute_values.grid.toggle_enable("publish_as_tag",(frm.doc.applicable_to_all)? false: true);
		frm.refresh_fields('item_attribute_values');
	},
	applicable_to_all: function(frm) {
		frm.fields_dict.item_attribute_values.grid.toggle_enable("publish_as_tag",(frm.doc.applicable_to_all)? false: true);
		
		frm.refresh_fields('item_attribute_values');

		frappe.call({
			method: 'dynamic_closure.customizations.item_attribute.item_attribute.publish_all_tags',
			args: {
                "item_attribute": frm.doc.name
            },
			callback: (r) => {
				if(r.message)
				{
					frappe.msgprint("Tag published successfully")
					frm.save()
				}
			}
		});
	}
});

frappe.ui.form.on('Item Attribute Value', {
	publish_as_tag: function(frm, cdt, cdn) {
		// let me = this;
		var row = locals[cdt][cdn]
		if(row.publish_as_tag)
		{
			
			frappe.call({
				method: 'dynamic_closure.customizations.item_attribute.item_attribute.publish_tags',
				args: {
	                "item_attribute": frm.doc.name,
	                "tagname": row.attribute_value
	            },
				callback: (r) => {
					if(r.message)
					{
						frappe.msgprint("Tag published successfully")
						frm.save()
					}
				}
			});
		}
	}

});

