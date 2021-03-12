$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-variety .modal-content").html("");
        $("#modal-variety").modal("show");
      },
      success: function (data) {
        $("#modal-variety .modal-content").html(data.html_form);
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
          $("#modal-variety").modal("hide");
          location.reload();
        }
        else {
          $("#modal-variety .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Crop Species
  $("#variety-table").on("click", ".js-edit-variety", loadForm);
  $("#modal-variety").on("submit", ".js-variety-update-form", saveForm);

  // Delete Crop Species
  $("#variety-table").on("click", ".js-delete-variety", loadForm);
  $("#modal-variety").on("submit", ".js-variety-delete-form", saveForm);

});
