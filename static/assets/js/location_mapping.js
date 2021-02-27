$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-location .modal-content").html("");
        $("#modal-location").modal("show");
      },
      success: function (data) {
        $("#modal-location .modal-content").html(data.html_form);
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
          $("#modal-location").modal("hide");
          location.reload();
        }
        else {
          $("#modal-location .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#location-table").on("click", ".js-edit-location", loadForm);
  $("#modal-location").on("submit", ".js-location-update-form", saveForm);

  // Delete Division
  $("#location-table").on("click", ".js-delete-location", loadForm);
  $("#modal-location").on("submit", ".js-location-delete-form", saveForm);

});
