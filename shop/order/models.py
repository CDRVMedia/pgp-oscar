from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.loading import get_model
from django.utils.translation import ugettext as _
from oscar.apps.address.abstract_models import AbstractShippingAddress
from oscar.apps.order.abstract_models import AbstractOrder
from pgp.shop.address.mixins import MinecraftAddressMixin
from pgp.shop.basket.models import Basket


Country = get_model('address', 'Country')
    
class Order(AbstractOrder):
    # if developer is deleted, the order remains with developer=None
    developer = ForeignKey('developer.Developer', blank=True, null=True,
                           on_delete=models.SET_NULL, verbose_name=_("Developer"))
    
    @property
    def basket(self):
        try:
            return Basket.objects.get(id=self.basket_id)
        except Basket.DoesNotExist:
            return None
    
    def save(self, *args, **kwargs):
        self.developer = self.developer or self.basket.developer
        return super(Order, self).save(*args, **kwargs)        


class ShippingAddress(MinecraftAddressMixin, AbstractShippingAddress):

    def save(self, *args, **kwargs):
        self.last_name = self.last_name if self.last_name else ''
        self.country = Country.objects.get(pk='UN')
        self.postcode = self.postcode if self.postcode else 0
        return super(ShippingAddress, self).save(*args, **kwargs)
    
# this must remain at the bottom of this file - comment out before doing auto import    
from oscar.apps.order.models import *  # @UnusedWildImport
