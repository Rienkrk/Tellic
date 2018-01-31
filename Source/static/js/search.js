// Gets an input, makes an ajax call which returns a list of phones and displays those in the view.
function myFunction(value, redirectedFrom) {

  // Trim the given value.
	value = value.trim();

	// Empty the html view list.
	$(".search-drop").empty();
	$(".results").empty();

  // Make a ajax call with json, whom return a list of related phones.
	$.ajax({
      url: '/search',
			data: {searchText: value},
			dataType: "json",

      // When succesfull run the respone function.
      success: function(response) {

					// Empty the html view list.
					$( ".search-drop" ).empty();
					$(".results").empty();

					// Check if there are results if not, return a error message else show results.
					if(response.phones == "No Matching Results Found.") {
						var html = "<span class='error'>Geen resultaten gevonden!</span>"

						// Check from which page the message came and display the results accordingly.
						if(redirectedFrom == "createReply") {
							$(".results").prepend(html);
						}
						else {
							$(".search-drop").prepend(html);
						};

					}
					else {

						// Loop trought each result and display the brand and devicename.
						for(x in response.phones){
							var phone = response.phones[x]['DeviceName']
							var brand = response.phones[x]['Brand']

							// Make sure the phone is not undefined.
							if (phone !== undefined) {

                // Check from which page the message came and display the results accordingly.
								if(redirectedFrom == "createReply") {
									var html = "<span id='"+phone+"' class='phoneReply'>"+phone+"</span>"
									$(".results").prepend(html);
								}
								else {
									var html = "<a href=\"/display/"+phone+"\"><span>" + phone + "</span></a>"
									$(".search-drop").prepend(html);
								};

							};

						};

					};

      },

			// If the response was not succesfull return the message that something went wrong.
      error: function(error) {
				var html = "<span class='error'>Er ging iets goed mis!</span>"
				
				// Check from which page the message came and display the results accordingly.
				if(redirectedFrom == "createReply") {
					$(".results").prepend(html);
				}
				else {
					$(".search-drop").prepend(html);
				};

      }

  });

};

// When a certain phone element from results is clicked, add the phone to the reply.
$(document).on('click', '.phoneReply', function(){
	$(".selected-phone").text(this.id);
	$("#phoneInput").val(this.id);
});
