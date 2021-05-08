$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book .modal-content").html("");
        $('#modal-book').modal('show');
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
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
          $("#inspection-details-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
      }
    });
    return false;
  };

  /* Binding */

  // Update Division
  $("#inspection-details-table").on("click", ".js-edit-details", loadForm);
  $("#modal-book").on("submit", ".js-feasibility-update-form", saveForm);

});
