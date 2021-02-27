$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-fodder-variety .modal-content").html("");
        $("#modal-fodder-variety").modal("show");
      },
      success: function (data) {
        $("#modal-fodder-variety .modal-content").html(data.html_form);
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
          $("#modal-fodder-variety").modal("hide");
          location.reload();
        }
        else {
          $("#modal-fodder-variety .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#fodder-variety-table").on("click", ".js-edit-fodder-variety", loadForm);
  $("#modal-fodder-variety").on("submit", ".js-fodder-variety-update-form", saveForm);

  // Delete Division
  $("#fodder-variety-table").on("click", ".js-delete-fodder-variety", loadForm);
  $("#modal-fodder-variety").on("submit", ".js-fodder-variety-delete-form", saveForm);


});
