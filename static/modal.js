function subscribe() {
  $.ajax({
    url: "/subscribe",
    type: "POST",
    data: $("#email").val(),
    success: function () {
      $(".modal-header").children("h5").text("Success!");
      $(".modal-body").children("p").text("Thank you for subscribing!");
      $("#modal-button").removeClass("btn-danger");
      $("#modal-button").addClass("btn-success");
    },
    error: function () {
      $(".modal-header").children("h5").text("Oops!");
      $(".modal-body").children("p").text("Invalid email!");
      $("#modal-button").removeClass("btn-success");
      $("#modal-button").addClass("btn-danger");
    },
    complete: function () {
      $(".modal").modal("show");
    }
  });
};
