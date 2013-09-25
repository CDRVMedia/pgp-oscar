from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext as _ 
from oscar.apps.partner.abstract_models import AbstractPartner


class Partner(AbstractPartner):
    game = OneToOneField('game.Game', related_name="partner", verbose_name=_("Game"))

# this must remain at the bottom of this file - comment out before doing auto import        
from oscar.apps.partner.models import *  # @UnusedWildImport
