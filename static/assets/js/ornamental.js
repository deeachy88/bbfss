$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-ornamental .modal-content").html("");
        $("#modal-ornamental").modal("show");
      },
      success: function (data) {
        $("#modal-ornamental .modal-content").html(data.html_form);
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
          $("#modal-ornamental").modal("hide");
          location.reload();
        }
        else {
          $("#modal-ornamental .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#ornamental-table").on("click", ".js-edit-ornamental", loadForm);
  $("#modal-ornamental").on("submit", ".js-ornamental-update-form", saveForm);

  // Delete Division
  $("#ornamental-table").on("click", ".js-delete-ornamental", loadForm);
  $("#modal-ornamental").on("submit", ".js-ornamental-delete-form", saveForm);


});
