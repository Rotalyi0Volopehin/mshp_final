from main.db_tools.game_session_tools import DBGameSessionTools
from main.db_tools.user_participation_tools import DBUserParticipationTools
from main.db_tools.user_tools import DBUserTools
from main.views.menu import get_menu_context, get_user_menu_context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from game_eng.market import Market


class DarknetCard:

    def __init__(self, name, tag, price, count):
        self.name = name
        self.tag = tag
        self.price = price
        self.count = count


@login_required
def darknet_page(request):
    context = {
        'pagename': 'DarkNet',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }

    user_participation = DBUserParticipationTools.get_user_participation(request.user)
    if user_participation is None:
        context['error'] = 'В данный момент вам не доступен DarkNet!'
        return render(request, 'pages/darknet.html', context)
    game_session = user_participation.game_session
    game_model = DBGameSessionTools.try_load_session_model(game_session)
    player = DBUserTools.try_get_player_of_user_from_game_model(request.user, game_model)

    assortment = game_model.market.assortment

    market_assortment = []
    for tool_type in Market.tool_types:
        market_assortment.append(assortment[tool_type])
    darknet_cards = []
    for slot in market_assortment:
        tag = slot.pt_set.__module__.split('.')[-1]
        darknet_cards.append(DarknetCard(slot.pt_set.name, tag, slot.price, slot.pt_set.count))
    context['darknet_cards'] = darknet_cards
    context['fraction_money'] = game_model.teams[player.team].money

    if request.method == 'POST':
        buy_product = request.POST.get('buy_product', None)
        if buy_product is not None:
            for tool_type in Market.tool_types:
                slot = assortment[tool_type]
                tool_tag = slot.pt_set.__module__.split('.')[-1]
                if buy_product == tool_tag:
                    Market.try_buy(player, tool_type, 1)
                    break

    return render(request, 'pages/darknet.html', context)
