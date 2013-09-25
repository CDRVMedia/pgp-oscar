from oscar.apps.checkout.app import \
    CheckoutApplication as BaseCheckoutApplication
from pgp.shop.checkout.views import ShippingAddressView, PaymentDetailsView

class CheckoutApplication(BaseCheckoutApplication):
    shipping_address_view = ShippingAddressView
    payment_details_view = PaymentDetailsView

application = CheckoutApplication()