function myFunction(value) {
	value = value.trim();
	$( ".search-drop" ).empty();
	$.ajax({
      url: '/search',
			data: {searchText: value},
			dataType: "json",
      success: function(response) {
          console.log(response.phones);

					for(x in response.phones){
						console.log(response.phones[x]["DeviceName"])
						var phone = response.phones[x]['DeviceName']
						var html = "<li class='list-group-item d-flex justify-content-between align-items-center'>" + phone + "<span class='badge badge-primary badge-pill'>14</span></li>"
						$(".search-drop").prepend(html);
					};

      },
      error: function(error) {
          console.log(error);
      }
  });

};
