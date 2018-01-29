$( document ).ready(function() {

  $( ".nav-link" ).click(function() {
    $(".pagination-wrapper").addClass("none");
    $("." + this.id).toggleClass("none");
    $(".nav-link").removeClass("focus-bg");
    $(this).addClass("focus-bg");
  });

});
