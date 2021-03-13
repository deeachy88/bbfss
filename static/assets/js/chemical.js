$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-chemical .modal-content").html("");
        $("#modal-chemical").modal("show");
      },
      success: function (data) {
        $("#modal-chemical .modal-content").html(data.html_form);
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
          $("#modal-chemical").modal("hide");
          location.reload();
        }
        else {
          $("#modal-chemical .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#chemical-table").on("click", ".js-edit-chemical", loadForm);
  $("#modal-chemical").on("submit", ".js-chemical-update-form", saveForm);

  // Delete Division
  $("#chemical-table").on("click", ".js-delete-chemical", loadForm);
  $("#modal-chemical").on("submit", ".js-chemical-delete-form", saveForm);
});
