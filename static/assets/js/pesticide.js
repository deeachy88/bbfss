$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-pesticide .modal-content").html("");
        $("#modal-pesticide").modal("show");
      },
      success: function (data) {
        $("#modal-pesticide .modal-content").html(data.html_form);
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
          $("#modal-pesticide").modal("hide");
          location.reload();
        }
        else {
          $("#modal-pesticide .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#pesticide-table").on("click", ".js-edit-pesticide", loadForm);
  $("#modal-pesticide").on("submit", ".js-pesticide-update-form", saveForm);

  // Delete Division
  $("#pesticide-table").on("click", ".js-delete-pesticide", loadForm);
  $("#modal-pesticide").on("submit", ".js-pesticide-delete-form", saveForm);
});