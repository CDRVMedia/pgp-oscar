from django.forms.fields import CharField
from django.utils.translation import ugettext as _
from oscar.apps.checkout.forms import ShippingAddressForm
from pgp.shop.address.models import UserAddress

class DeliveryPlayerForm(ShippingAddressForm):
    
    def __init__(self, *args, **kwargs):
        super(DeliveryPlayerForm, self).__init__(*args, **kwargs)
        uid_field = getattr(UserAddress, 'uid_field')
        self.fields = {uid_field: CharField(label=_('Minecraft Player'))}
        
