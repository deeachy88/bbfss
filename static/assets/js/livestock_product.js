$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-common .modal-content").html("");
        $("#modal-common").modal("show");
      },
      success: function (data) {
        $("#modal-common .modal-content").html(data.html_form);
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
          $("#modal-common").modal("hide");
          location.reload();
        }
        else {
          $("#modal-common .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */

  // Update Product
  $("#livestock-product-table").on("click", ".js-edit-livestock-product", loadForm);
  $("#modal-common").on("submit", ".js-livestock-product-update-form", saveForm);

  // Delete Product
  $("#livestock-product-table").on("click", ".js-delete-livestock-product", loadForm);
  $("#modal-common").on("submit", ".js-livestock-product-delete-form", saveForm);


});
