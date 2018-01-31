// Only run function inside when the document is ready.
$(document).ready(function() {

  // When a certain class is clicked do the following;
  $( ".nav-link" ).click(function() {

    // Display only the clicked page.
    $(".pagination-wrapper").addClass("none");
    $("." + this.id).toggleClass("none");

    // Change the style of the pagination controller.
    $(".nav-link").removeClass("focus-bg");
    $(this).addClass("focus-bg");

  });

});
