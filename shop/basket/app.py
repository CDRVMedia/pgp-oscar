from oscar.apps.basket.app import BasketApplication as BaseBasketApplication
from pgp.shop.basket.views import BasketView, SavedView

class BasketApplication(BaseBasketApplication):
    summary_view = BasketView
    saved_view = SavedView    

application = BasketApplication()