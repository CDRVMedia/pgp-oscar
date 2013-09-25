from pgp.account.models import MinecraftAccount
from pgp.settings import DEFAULT_USER_AVATAR

class MinecraftAddressMixin(object):
    uid_field = 'line1'
    _avatar_url = None
    
    @property
    def avatar_url(self):
        if not self._avatar_url:
            try:
                mca = MinecraftAccount.objects.get_for_playername(self.uid)
                self._avatar_url = mca.get_avatar_url()
            except MinecraftAccount.DoesNotExist:
                self._avatar_url = DEFAULT_USER_AVATAR
        return self._avatar_url
        
    @property
    def uid(self): return getattr(self, self.uid_field)
