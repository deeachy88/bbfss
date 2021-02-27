$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-crop .modal-content").html("");
        $("#modal-crop").modal("show");
      },
      success: function (data) {
        $("#modal-crop .modal-content").html(data.html_form);
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
          $("#modal-crop .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#crop-table").on("click", ".js-edit-crop", loadForm);
  $("#modal-crop").on("submit", ".js-crop-update-form", saveForm);

  // Delete Division
  $("#crop-table").on("click", ".js-delete-crop", loadForm);
  $("#modal-crop").on("submit", ".js-crop-delete-form", saveForm);

});
