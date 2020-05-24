function set_cards_state(cards_class, state) {
    for (let el of document.querySelectorAll('.' + cards_class)) {
        el.style.visibility = state;
        if (state == 'visible')
            el.style.display = "block";
        else
            el.style.display = "none";
    }
}

function hide_all_cards() {
    set_all_cards_state('hidden');
}

function show_all_cards() {
    set_all_cards_state('visible');
}

function button_all() {
   show_all_cards();
}