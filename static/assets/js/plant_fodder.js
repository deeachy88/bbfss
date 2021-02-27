$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-plant-fodder .modal-content").html("");
        $("#modal-plant-fodder").modal("show");
      },
      success: function (data) {
        $("#modal-plant-fodder .modal-content").html(data.html_form);
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
          $("#modal-plant-fodder").modal("hide");
          location.reload();
        }
        else {
          $("#modal-plant-fodder .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#plant-fodder-table").on("click", ".js-edit-plant-fodder", loadForm);
  $("#modal-plant-fodder").on("submit", ".js-plant-fodder-update-form", saveForm);

  // Delete Division
  $("#plant-fodder-table").on("click", ".js-delete-plant-fodder", loadForm);
  $("#modal-plant-fodder").on("submit", ".js-plant-fodder-delete-form", saveForm);
});
