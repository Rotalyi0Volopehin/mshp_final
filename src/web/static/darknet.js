function set_cards_state(cards_class, state) {
    for (let el of document.querySelectorAll('.' + cards_class)) {
        el.style.visibility = state;
        if (state == 'visible')
            el.style.display = "block";
        else
            el.style.display = "none";
    }
}

function set_all_cards_state(state) {
    set_cards_state('tool-attack', state);
    set_cards_state('tool-protection', state);
    set_cards_state('tool-mining', state);
    set_cards_state('tool-antivirus', state);
    set_cards_state('tool-kamikaze', state);
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

function button_attack() {
    hide_all_cards();
    set_cards_state('tool-attack', 'visible');
}

function button_protection() {
    hide_all_cards();
    set_cards_state('tool-protection', 'visible');
}

function button_mining() {
    hide_all_cards();
    set_cards_state('tool-mining', 'visible');
}

function button_antivirus() {
    hide_all_cards();
    set_cards_state('tool-antivirus', 'visible');
}

function button_kamikaze() {
    hide_all_cards();
    set_cards_state('tool-kamikaze', 'visible');
}