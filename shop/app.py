from django.conf.urls import patterns, include
from oscar.app import Shop
from pgp.shop.catalogue.app import application as catalogue_app
from pgp.shop.checkout.app import application as checkout_app
from pgp.shop.customer.app import application as customer_app
from pgp.shop.dashboard.app import application as dashboard_app
from pgp.shop.dashboard.express.app import application as express_app
from pgp.shop.basket.app import application as basket_app
from pgp.shop.paypal.app import application as paypal_app

class BaseShop(Shop):
    dashboard_app = dashboard_app
    catalogue_app = catalogue_app
    checkout_app = checkout_app
    customer_app = customer_app
    basket_app = basket_app
    paypal_app = paypal_app
    
    @property
    def subdomain_urls(self): return self.get_subdomain_urls(), self.app_name, self.name
    @property
    def admin_urls(self): return self.get_admin_urls(), self.app_name, self.name
        
    
    def get_urls(self):
        urlpatterns = patterns('',
            (r'', include(self.promotions_app.urls)),
        )
        return urlpatterns
    
    def get_subdomain_urls(self):
        urlpatterns = patterns('',
            (r'^basket/', include(self.basket_app.urls)),
            (r'^checkout/', include(self.checkout_app.urls)),
            (r'^checkout/paypal/', include(self.paypal_app.urls)),
            (r'^accounts/', include(self.customer_app.urls)),
            (r'^search/', include(self.search_app.urls)),
            (r'^offers/', include(self.offer_app.urls)),
            # (r'^customer/', include(self.customer_app.urls)),
            (r'', include(self.catalogue_app.urls)),

            (r'', include(self.promotions_app.urls)),
        )
        for resolver in urlpatterns:
            resolver.app_name = 'shop'
        return urlpatterns
    
    def get_admin_urls(self):
        urlpatterns = patterns('',
            (r'^dashboard/', include(self.dashboard_app.urls)),
            # paypal express is included in the dashboard app but including it again because urls in paypal templates are not scoped to dashboard:
            (r'^dashboard/express/', include(express_app.urls)),
        )
        return urlpatterns
    
shop = BaseShop()


