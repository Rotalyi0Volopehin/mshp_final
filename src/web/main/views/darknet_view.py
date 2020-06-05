from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.db_tools.game_session_tools import DBGameSessionTools
from main.db_tools.user_participation_tools import DBUserParticipationTools
from main.db_tools.user_tools import DBUserTools
from main.views.menu import get_menu_context, get_user_menu_context
from game_eng.market import Market


class DarknetCard:

    def __init__(self, name, tag, price, count, availability):
        self.name = name
        self.tag = tag
        self.price = price
        self.count = count
        self.availability = availability


def get_db_page_data(request):
    view_mode = False

    user_participation = DBUserParticipationTools.get_user_participation(request.user)
    if user_participation is None:
        view_mode = True
        return view_mode, None, None

    game_session = user_participation.game_session
    if game_session is None:
        view_mode = True
        return view_mode, None, None

    game_model, error = DBGameSessionTools.try_load_game_model(game_session)
    if game_session is None:
        view_mode = True
        return view_mode, None, None
    if error is not None:
        view_mode = True
        return view_mode, None, None

    player = DBUserTools.try_get_player_of_user_from_game_model(request.user, game_model)
    if player is None:
        view_mode = True
        return view_mode, None, None

    market = game_model.market
    if market is None:
        view_mode = True
        return view_mode, None, None

    team_money = player.team.money
    if team_money is None:
        view_mode = True
        return view_mode, None, None

    return view_mode, player, market


@login_required
def darknet_page(request):
    context = {
        'pagename': 'DarkNet',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    view_mode, player, market = get_db_page_data(request)
    context['view_mode'] = view_mode

    if view_mode:
        market = Market()
    else:
        team_money = player.team.money
        context['fraction_money'] = team_money
    assortment = market.assortment

    market_assortment = []
    for tool_type in Market.tool_types:
        market_assortment.append(assortment[tool_type])
    darknet_cards = []
    for slot in market_assortment:
        tag = slot.pt_set.__module__.split('.')[-1]
        if view_mode:
            availability = False
            count = '∞'
        else:
            availability = True if team_money >= slot.price else False
            count = slot.pt_set.count
        darknet_cards.append(DarknetCard(slot.pt_set.name, tag, slot.price, count, availability))
    context['darknet_cards'] = darknet_cards

    if request.method == 'POST':
        if not view_mode:
            buy_product = request.POST.get('buy_product', None)
            if buy_product is not None:
                for tool_type in Market.tool_types:
                    slot = assortment[tool_type]
                    tool_tag = slot.pt_set.__module__.split('.')[-1]
                    if buy_product == tool_tag:
                        res = market.try_buy(player, tool_type, 1)
                        if not res:
                            context['warning'] = 'У вас недостаточно денег для покупки!'
                        break

    return render(request, 'pages/darknet.html', context)
