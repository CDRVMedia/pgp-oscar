from django.db.models.manager import Manager
from oscar.apps.address.abstract_models import AbstractUserAddress
from pgp.shop.address.mixins import MinecraftAddressMixin



class UserAddressManager(Manager):
    unknown_country = None
    
    def get_or_create(self, **kwargs):
        try:
            obj = self.get(**kwargs)
            return obj, False
        except UserAddress.DoesNotExist:
            obj = self.create(**kwargs)
            return obj, True
    
    def create(self, **kwargs):
        assert 'user' in kwargs, 'user must be specified when creating a UserAddress'
        return super(UserAddressManager, self).create(**kwargs)
    

class UserAddress(MinecraftAddressMixin, AbstractUserAddress):
    objects = UserAddressManager()

    def active_address_fields(self):
        """
        Returns the fields relevant to PGP
        """
        self._clean_fields()
        fields = [self.line1]

        return fields
    
    def save(self, *args, **kwargs):
        # initialize required fields if needed
        if not self.last_name:
            if hasattr(self, 'user') and self.user:
                self.first_name = self.user.first_name
                self.last_name = self.user.last_name
            else:
                self.first_name = self.last_name = ''
        self.country = self.country if self.country else Country.objects.get(pk='UN')
        return super(UserAddress, self).save(*args, **kwargs)
    

# this must remain at the bottom of this file - comment out before doing auto import    
from oscar.apps.address.models import *  # @UnusedWildImport