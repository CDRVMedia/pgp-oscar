from django.db.models.fields.related import ForeignKey
from oscar.apps.basket.abstract_models import AbstractBasket
from django.utils.translation import ugettext as _
from django.db import models

class Basket(AbstractBasket):
    # developer can be null in the case where this is a cookie basket at the root domain
    developer = ForeignKey('developer.Developer', blank=True, null=True,
                           on_delete=models.SET_NULL, verbose_name=_("Developer"))
    
    def __init__(self, *args, **kwargs):
        super(Basket, self).__init__(*args, **kwargs)
        

# this must remain at the bottom of this file - comment out before doing auto import    
from oscar.apps.basket.models import *  # @UnusedWildImport
