$('#myModal').on('shown.bs.modal', function () {
        $('#myInput').trigger('focus')
    })

function progress_bar() {
    document.getElementById('progress-bar').style.width = exp + '%';
}
function clear_pw_change_form() {
    OldPassword.value = "";
    NewPassword.value = "";
    NewPassword2.value = "";
}
function check_pw_change() {
    if (NewPassword.value != NewPassword2.value) {
        save_pw_tag.disabled = true;
        change_pw_button_footer.hidden = true;
        change_pw_warning_footer.hidden = false;
    }
}
function close_pw_warning() {
    save_pw_tag.disabled = false;
    change_pw_warning_footer.hidden = true;
    change_pw_button_footer.hidden = false;
}