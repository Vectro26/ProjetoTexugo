$(function() {
	$("#tabs").tabs();
    $("#autocompleteSearch").autocomplete({
        source: '/autocomplete',
        minLength: 3,
    });
	/*
	 * TODo esto tardaba bocha y por eso se lo comento...
	$("#selectableAllClasses").selectable({
		stop: function(event, ui) {
			var selected_package = $(".ui-selected", this).attr('id');
			$("#selected_package").val(selected_package);
		}
	});	
	*/
	
	// TODO seguir la parte del JS desde aca...
    /*
    $("#package_tree").treeview({	
		toggle: function() {
			ajax: {
				type: "get",
				data: {
					//
				}
			}
		}		
	});
    */
});

