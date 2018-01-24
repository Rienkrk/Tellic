function myFunction(value) {
	value = value.trim();
	$( "#lachen" ).empty();
	$.ajax({
      url: '/search',
			data: {searchText: value},
			dataType: "json",
      success: function(response) {
          console.log(response.phones);

					for(x in response.phones){
						console.log(response.phones[x]["DeviceName"])
						$("#lachen").prepend(response.phones[x]["DeviceName"]);
					};

      },
      error: function(error) {
          console.log(error);
      }
  });

};
