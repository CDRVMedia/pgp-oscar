from oscar.apps.basket.views import BasketView as BaseBasketView, SavedView as BaseSavedView

def get_basket_queryset(basket, game):
        return basket.all_lines().filter(product__partner=game.partner)

class BasketView(BaseBasketView):
    pass


class SavedView(BaseSavedView):
    pass
