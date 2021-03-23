$(function () {
alert("ong");
  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-decision .modal-content").html("");
        $('#modal-decision').modal('show');
      },
      success: function (data) {
        $("#modal-decision .modal-content").html(data.html_form);
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
          $("#modal-decision").modal("hide");

        }
        else {
          $("#modal-decision .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#decision-table").on("click", ".js-edit", loadForm);
  $("#modal-decision").on("submit", ".js-decision-update-form", saveForm);

});
