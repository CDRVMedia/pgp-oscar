from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from oscar.core.application import Application
from pgp.shop.paypal.express.app import application as express_app


class PayPalApplication(Application):
    express_app = express_app

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'', include(self.express_app.urls)),
        )
        return urlpatterns

application = PayPalApplication()
