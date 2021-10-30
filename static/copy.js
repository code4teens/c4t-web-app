function copy(elem) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(elem).siblings('input').val()).select();
  document.execCommand("copy");
  $temp.remove();
}

$(function () {
  $('[data-bs-toggle="tooltip"]').tooltip({
    trigger: "click",
    placement: "left",
    title: "Copied to clipboard!"
  })
})

$('[data-bs-toggle="tooltip"]').on('shown.bs.tooltip', function () {
  setTimeout(function () {
    $('[data-bs-toggle="tooltip"]').tooltip("hide")
  }, 500)
})