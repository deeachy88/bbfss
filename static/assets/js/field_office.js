$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-field-office .modal-content").html("");
        $("#modal-field-office").modal("show");
      },
      success: function (data) {
        $("#modal-field-office .modal-content").html(data.html_form);
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
          $("#modal-field-office").modal("hide");
          location.reload();
        }
        else {
          $("#modal-field-office .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#field-office-table").on("click", ".js-edit-field-office", loadForm);
  $("#modal-field-office").on("submit", ".js-field-office-update-form", saveForm);

  // Delete Division
  $("#field-office-table").on("click", ".js-delete-field-office", loadForm);
  $("#modal-field-office").on("submit", ".js-field-office-delete-form", saveForm);

});
