from oscar.core.loading import get_class
from paypal.express.views import SuccessResponseView as BaseSuccessResponseView

PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')


class SuccessResponseView(BaseSuccessResponseView):
    ''' override to use the standard (or our) create_shipping_address methods '''
    def create_shipping_address(self, basket=None):
        return super(BaseSuccessResponseView, self).create_shipping_address(basket)
    
    def get_shipping_method(self, basket=None):
        return super(BaseSuccessResponseView, self).get_shipping_method(basket)
    
    def get_context_data(self, **kwargs):
        ''' override shipping method with original (our) shipping method '''
        ctx = super(SuccessResponseView, self).get_context_data(**kwargs)
        ctx['shipping_address'] = super(BaseSuccessResponseView, self).get_shipping_address()
        return ctx