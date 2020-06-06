function min_limit_checkbox_clicked() {
    id_user_min_level.disabled = !id_min_level_limit_existence.checked;
    id_user_min_level.required = id_min_level_limit_existence.checked;
}

function max_limit_checkbox_clicked() {
    id_user_max_level.disabled = !id_max_level_limit_existence.checked;
    id_user_max_level.required = id_max_level_limit_existence.checked;
}