function check_pw() {
    if (id_password1.value != id_password2.value) {
        reg_button.disabled = true;
        reg_button.hidden = true;
        pw_warning.hidden = false;
    }
}
function close_pw_warning() {
    reg_button.disabled = false;
    pw_warning.hidden = true;
    reg_button.hidden = false;
}