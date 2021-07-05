$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-food .modal-content").html("");
        $("#modal-food").modal("show");
      },
      success: function (data) {
        $("#modal-food .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-crop").modal("hide");
          location.reload();
        }
        else {
          $("#modal-food .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Crop
  $("#food-table").on("click", ".js-edit-food_handler", loadForm);
  $("#modal-food").on("submit", ".js-crop-update-form", saveForm);


});
