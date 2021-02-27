$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-user .modal-content").html("");
        $("#modal-user").modal("show");
      },
      success: function (data) {
        $("#modal-user .modal-content").html(data.html_form);
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
          $("#modal-user").modal("hide");
          location.reload();
        }
        else {
          $("#modal-user .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

var loadRoleForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-role .modal-content").html("");
        $("#modal-role").modal("show");
      },
      success: function (data) {
        $("#modal-role .modal-content").html(data.html_form);
      }
    });
  };

  var saveRoleForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-role").modal("hide");
          location.reload();
        }
        else {
          $("#modal-role .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  
  var loadDeleteForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-role-delete .modal-content").html("");
        $("#modal-role-delete").modal("show");
      },
      success: function (data) {
        $("#modal-role-delete .modal-content").html(data.html_form);
      }
    });
  };
  
  var deleteRoleForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-role-delete").modal("hide");
          location.reload();
        }
        else {
          $("#modal-role-delete .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  
  

  
  

  // Update user
  $("#user-table").on("click", ".js-update-book", loadForm);
  $("#modal-user").on("submit", ".js-book-update-form", saveForm);

  // Update role
  $("#role-table").on("click", ".js-edit-role", loadRoleForm);
  $("#modal-role").on("submit", ".js-role-update-form", saveRoleForm);
  $("#role-table").on("click", ".js-delete-role", loadRoleForm);
  $("#modal-role").on("submit", ".js-role-delete-form", saveRoleForm);
});


function noBack()
{
    window.history.forward();
}


