$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				url : $('#url').val(),
				
			},
			type : 'POST',
			url : '/collect'
		})
		.done(function(data) {

			if (data.error) {
            alert('error')    
            }
			else {
                alert('sucess') 
			}

		});

		event.preventDefault();

	});

});
