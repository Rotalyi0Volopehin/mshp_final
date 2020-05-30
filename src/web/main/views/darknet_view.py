from main.views.menu import get_menu_context, get_user_menu_context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from game_eng.market import Market


@login_required
def darknet_page(request):
    context = {
        'pagename': 'DarkNet',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }

    # === temp ===
    m = Market()
    m.collect_tool_types()
    assortment = m.assortment
    # ============

    if request.method == 'POST':
        buy_product = request.POST.get('buy_product', None)
        if buy_product is not None:
            buy_type = None
            for t in Market.tool_types:
                if t.name == buy_product:
                    buy_type = t
            # m.try_buy(request.user, buy_type, 1)

    context['tool_types'] = Market.tool_types
    context['assortment'] = assortment
    return render(request, 'pages/darknet.html', context)
