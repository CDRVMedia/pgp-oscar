from django.conf import settings
from django.db.models import get_model
from oscar.apps.basket.middleware import BasketMiddleware as BaseBasketMiddleware
from oscar.core.loading import get_class
import zlib


Applicator = get_class('offer.utils', 'Applicator')
Basket = get_model('basket', 'basket')


class BasketMiddleware(BaseBasketMiddleware):
    '''
    override so we can add request.game into the basket for line filtering
    '''
    def get_basket(self, request):
        cookie_key = self.get_cookie_key(request.developer)
        manager = Basket.open
        cookie_basket = self.get_cookie_basket(
            cookie_key, request, manager)

        if hasattr(request, 'user') and request.user.is_authenticated():
            # Signed-in user: if they have a cookie basket too, it means
            # that they have just signed in and we need to merge their cookie
            # basket into their user basket, then delete the cookie
            try:
                basket, _ = manager.get_or_create(owner=request.user, developer=request.developer)
            except Basket.MultipleObjectsReturned:
                # Not sure quite how we end up here with multiple baskets
                # We merge them and create a fresh one
                old_baskets = list(manager.filter(owner=request.user, developer=request.developer))
                basket = old_baskets[0]
                for other_basket in old_baskets[1:]:
                    self.merge_baskets(basket, other_basket)

            # Assign user onto basket to prevent further SQL queries when
            # basket.owner is accessed.
            basket.owner = request.user
            basket.developer = request.developer

            if cookie_basket:
                self.merge_baskets(basket, cookie_basket)
                request.cookies_to_delete.append(
                    cookie_key)
        elif cookie_basket:
            # Anonymous user with a basket tied to the cookie
            basket = cookie_basket
        else:
            # Anonymous user with no basket - we don't save the basket until
            # we need to.
            basket = Basket(developer=request.developer)
        return basket

    def get_cookie_basket(self, cookie_key, request, manager):
        """
        append the developer pk to the cookie_key so we can have a cookie basket for each developer
        """
        return super(BasketMiddleware, self).get_cookie_basket(cookie_key, request, manager)
        
    def get_cookie_key(self, developer, cookie_key=settings.OSCAR_BASKET_COOKIE_OPEN):
        if developer:
            return '%s-%s' % (cookie_key,
                              str(zlib.crc32(str(developer.id) + settings.SECRET_KEY)))
        else:
            return cookie_key
        
    def process_response(self, request, response):
        # Delete any surplus cookies
        if hasattr(request, 'cookies_to_delete'):
            for cookie_key in request.cookies_to_delete:
                response.delete_cookie(cookie_key)

        # If a basket has had products added to it, but the user is anonymous
        # then we need to assign it to a cookie
        cookie_key = self.get_cookie_key(request.developer)
        if (hasattr(request, 'basket') and request.basket.id > 0
            and not request.user.is_authenticated()
            and cookie_key not in request.COOKIES):
            cookie = "%s_%s" % (
                request.basket.id, self.get_basket_hash(request.basket.id))
            response.set_cookie(cookie_key,
                                cookie,
                                max_age=settings.OSCAR_BASKET_COOKIE_LIFETIME,
                                httponly=True)
        return response        
