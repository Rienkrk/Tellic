function myFunction(value) {
	value = value.trim();
	$( ".search-drop" ).empty();
	$.ajax({
      url: '/search',
			data: {searchText: value},
			dataType: "json",
      success: function(response) {
          console.log(response.phones);
					$( ".search-drop" ).empty();
					for(x in response.phones){
						console.log(response.phones[x])
						var phone = response.phones[x]['DeviceName']
						var brand = response.phones[x]['Brand']

						if (phone !== undefined) {
							var html = "<a href=\"/display/"+phone+"\"><li class='list-group-item d-flex justify-content-between align-items-center'>" + phone + "<span class='badge badge-primary badge-pill'>" + brand + "</span></li></a>"
							$(".search-drop").prepend(html);
						};

					};

      },
      error: function(error) {
          console.log(error);
      }
  });

};
