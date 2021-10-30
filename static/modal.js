function subscribe() {
  $.ajax({
    url: "/subscribe",
    type: "POST",
    data: $("#email").val(),
    success: function () {
      $(".modal-header").children("h5").text("Success!");
      $(".modal-body").children("p").text("Thank you for subscribing!");
    },
    error: function () {
      $(".modal-header").children("h5").text("Ooooooops!");
      $(".modal-body").children("p").text("Invalid email!");
    },
    complete: function () {
      $(".modal").modal("show");
    }
  });
};