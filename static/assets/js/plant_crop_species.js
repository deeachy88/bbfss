$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-species .modal-content").html("");
        $("#modal-species").modal("show");
      },
      success: function (data) {
        $("#modal-species .modal-content").html(data.html_form);
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
          $("#modal-species").modal("hide");
          location.reload();
        }
        else {
          $("#modal-species .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Crop Species
  $("#species-table").on("click", ".js-edit-crop-species", loadForm);
  $("#modal-species").on("submit", ".js-species-update-form", saveForm);

  // Delete Crop Species
  $("#species-table").on("click", ".js-delete-crop-species", loadForm);
  $("#modal-species").on("submit", ".js-species-delete-form", saveForm);

});
