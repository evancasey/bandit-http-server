$(function(){

	$('button').on('click', function(e){
	    e.preventDefault();

	    $.ajax({
			type: "POST",
			dataType: "json",
			url: $SCRIPT_ROOT + '/create',
			data: {"test_key": "test_value"},
			success: function (data) {
				console.log(data.test_key);
			},  			
		});

	});


});