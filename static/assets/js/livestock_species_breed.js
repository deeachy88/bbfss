$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-breed .modal-content").html("");
        $("#modal-breed").modal("show");
      },
      success: function (data) {
        $("#modal-breed .modal-content").html(data.html_form);
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
          $("#modal-breed").modal("hide");
          location.reload();
        }
        else {
          $("#modal-breed .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Crop Species
  $("#species-breed-table").on("click", ".js-edit-species-breed", loadForm);
  $("#modal-breed").on("submit", ".js-species-breed-update-form", saveForm);

  // Delete Crop Species
  $("#species-breed-table").on("click", ".js-delete-species-breed", loadForm);
  $("#modal-breed").on("submit", ".js-species-breed-delete-form", saveForm);

});
