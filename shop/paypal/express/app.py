from django.conf.urls import patterns
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from oscar.core.application import Application
from paypal.express.views import CancelResponseView
from paypal.express.views import RedirectView
from paypal.express.views import ShippingOptionsView
from pgp.shop.paypal.express.views import SuccessResponseView


class PayPalExpressApplication(Application):
    

    def get_urls(self):
        urlpatterns = patterns('',
            # Views for normal flow that starts on the basket page
            url(r'^redirect/', RedirectView.as_view(), name='paypal-redirect'),
            url(r'^preview/(?P<basket_id>\d+)/$', SuccessResponseView.as_view(preview=True), name='paypal-success-response'),
            url(r'^cancel/(?P<basket_id>\d+)/$', CancelResponseView.as_view(), name='paypal-cancel-response'),
            url(r'^place-order/(?P<basket_id>\d+)/$', SuccessResponseView.as_view(), name='paypal-place-order'),
            
            # Callback for getting shipping options for a specific basket
            url(r'^shipping-options/(?P<basket_id>\d+)/', csrf_exempt(ShippingOptionsView.as_view()), name='paypal-shipping-options'),
            # View for using PayPal as a payment method
            url(r'^payment/', RedirectView.as_view(as_payment_method=True), name='paypal-direct-payment'),
        )
        return urlpatterns

application = PayPalExpressApplication()
