""" Страница DarkNet'а """

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.db_tools.game_session_tools import DBGameSessionTools
from main.db_tools.user_participation_tools import DBUserParticipationTools
from main.db_tools.user_tools import DBUserTools
from main.views.menu import get_menu_context, get_user_menu_context

from game_eng.market import Market


class DarknetCard:
    """**Карточка товара на стринице даркнета**"""
    def __init__(self, name, tag, price, count, availability):
        self.name = name
        self.tag = tag
        self.price = price
        self.count = count
        self.availability = availability


def get_db_page_data(request):
    """**Получение данных из базы данных для страницы даркнета**\n
    :param request: request на страницу '/chat/'
    :type request: HttpRequest
    :return: набор данных для страницы
    :rtype: tuple
    """
    view_mode = False
    user_participation = DBUserParticipationTools.get_user_participation(request.user)
    if user_participation is None:
        view_mode = True
        return view_mode, None, None, None
    game_session = user_participation.game_session
    if game_session is None:
        view_mode = True
        return view_mode, None, None, None
    game_model, error = DBGameSessionTools.try_load_game_model(game_session)
    if game_session is None:
        view_mode = True
        return view_mode, None, None, None
    if error is not None:
        view_mode = True
        return view_mode, None, None, None
    player = DBUserTools.try_get_player_of_user_from_game_model(request.user, game_model)
    if player is None:
        view_mode = True
        return view_mode, None, None, None
    market = game_model.market
    if market is None:
        view_mode = True
        return view_mode, None, None, None
    team_money = player.team.money
    if team_money is None:
        view_mode = True
        return view_mode, None, None, None
    return view_mode, player, game_model, game_session


@login_required
def darknet_page(request):
    """**View функция даркнета**\n
    :param request: request на страницу 'darknet/'
    :type request: HttpRequest
    :return: response
    :rtype: HttpResponse
    """
    context = {
        'pagename': 'Darknet',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    view_mode, player, game_model, game_session = get_db_page_data(request)
    context['view_mode'] = view_mode

    if view_mode:
        market = Market()
    else:
        market = game_model.market
        context['fraction_money'] = player.team.money
    assortment = market.assortment

    if request.method == 'POST':
        if not view_mode:
            buy_product = request.POST.get('buy_product', None)
            if buy_product is not None:
                if game_model.current_team == player.team:
                    context["warning"] = "Дождитесь конца хода своей фракции!"
                else:
                    for tool_type in Market.tool_types:
                        slot = assortment[tool_type]
                        tool_tag = slot.pt_set.__module__.split('.')[-1]
                        if buy_product == tool_tag:
                            success = market.try_buy(player, tool_type, 1)
                            if success:
                                DBGameSessionTools.save_game_model(game_session, game_model)
                                context['fraction_money'] = player.team.money
                            else:
                                context['warning'] = 'Покупка невозможна!'
                            break

    darknet_cards = []
    for slot in market.assortment.values():
        tag = slot.pt_set.__module__.split('.')[-1]
        if view_mode:
            availability = False
            count = '-'
        else:
            count = slot.pt_set.count
            availability = (player.team.money >= slot.price) and (count > 0)
        darknet_cards.append(DarknetCard(slot.pt_set.name, tag, slot.price, count, availability))
    context['darknet_cards'] = darknet_cards

    return render(request, 'pages/darknet.html', context)
