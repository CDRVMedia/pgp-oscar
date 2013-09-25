from django.db.models.loading import get_model
from oscar.apps.checkout.views import \
    ShippingAddressView as BaseShippingAddressView, PaymentDetailsView as BasePaymentDetailsView
from pgp.account.models import MinecraftAccount
from pgp.shop.checkout.forms import DeliveryPlayerForm

UserAddress = get_model('address', 'UserAddress')

class ShippingAddressView(BaseShippingAddressView):
    form_class = DeliveryPlayerForm

    def get_available_addresses(self):
        # get a list of this user's minecraft account uids (player names)
        mc_account_uids = MinecraftAccount.objects.filter(user=self.request.user).values_list(MinecraftAccount.uid_field, flat=True)
        
        # delete any UserAddresses that don't match the user's list of mc accounts
        uid_field__in_kwargs = {UserAddress.uid_field + '__in':mc_account_uids}  # create a dict so we can construct the keyword 'key' in the filters below
        UserAddress._default_manager.filter(user=self.request.user).exclude(**uid_field__in_kwargs).delete()
        
        # add UserAddresses if any are missing
        for uid in mc_account_uids:
            uid_kwargs = {UserAddress.uid_field: uid}
            UserAddress.objects.get_or_create(user=self.request.user, **uid_kwargs)
        
        # finally, return the user's addresses now that addresses match accounts
        return UserAddress._default_manager.filter(user=self.request.user, **uid_field__in_kwargs)
            
            
class PaymentDetailsView(BasePaymentDetailsView):
    pass