from decimal import Decimal as D
from django.db.models.fields import CharField, DecimalField
from django.db.models.fields.related import ForeignKey
from django.db.models.loading import get_model
from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct, \
    AbstractCategory
from pgp import settings

Partner = get_model('partner', 'partner')

class Category(AbstractCategory):
    game = ForeignKey('game.Game')
    
    class Meta(AbstractCategory.Meta):
        unique_together = ('game', 'slug')     

    def save(self, update_slugs=True, *args, **kwargs):
        '''
        override to take out slug unique check which since
        slugs don't have to be unique in pgp.  game,slug is
        now a unique combo
        '''
        if update_slugs:
            parent = self.get_parent()
            slug = slugify(self.name)
            # If category has a parent, includes the parents slug in this one
            if parent:
                self.slug = '%s%s%s' % (
                    parent.slug, self._slug_separator, slug)
                self.full_name = '%s%s%s' % (
                    parent.full_name, self._full_name_separator, self.name)
            else:
                self.slug = slug
                self.full_name = self.name
                
        super(AbstractCategory, self).save(*args, **kwargs)      

class Product(AbstractProduct):
    # Price info:
    price_currency = CharField(
        _("Currency"), max_length=12, default=settings.OSCAR_DEFAULT_CURRENCY)

    # This is the base price for calculations - tax should be applied by the
    # appropriate method.  We don't store tax here as its calculation is highly
    # domain-specific.  It is NULLable because some items don't have a fixed
    # price but require a runtime calculation (possible from an external
    # service).
    price_excl_tax = DecimalField(
        _("Price (%(currency)s)") % {'currency': settings.OSCAR_DEFAULT_CURRENCY},
        decimal_places=2, max_digits=12)
    
    # products directly reference partner (partner aligns with game) since we do not have actual stock records
    partner = ForeignKey('partner.Partner', verbose_name=_("Partner")) 
    
    # properties
    @property
    def price_incl_tax(self): return self.price_excl_tax
        
    def __init__(self, *args, **kwargs):
        if hasattr(Product, 'stockrecord'):
            delattr(Product, 'stockrecord')  # remove the stockrecord field before super init
        super(Product, self).__init__(*args, **kwargs)
        # override stockrecord reverse relationship attribute to be pgp_stockrecord property
        if self.pk:
            self.stockrecord = self.StockRecord(product=self,
                                                partner=self.partner)
            
    @property
    def has_stockrecord(self):
        """
        Test if this product has a stock record
        """
        return True if hasattr(self, 'stockrecord') and self.stockrecord else False
    
    class StockRecord(object):
        '''
        PGP does not use stock records at the moment, so inner class creates a
        passive/transient object for the benefit of code that expects
        stock records.
        '''
        # these attributes replace StockRecord fields
        product = None    
        partner = None
        partner_sku = '0000'
        cost_price = D('0.00')
        low_stock_threshold = None
        @property
        def price_currency(self): return self.product.price_currency
        @property
        def price_excl_tax(self): return self.product.price_excl_tax
        @property
        def price_retail(self): return self.price_excl_tax
        @property
        def num_in_stock(self): return 9999
        @num_in_stock.setter
        def num_in_stock(self, value): pass
        @property
        def num_allocated(self): return 0
        @num_allocated.setter
        def num_allocated(self, value): pass
        
        # StockRecord Methods
        def __init__(self, *args, **kwargs):
            for k, v in kwargs.iteritems():
                setattr(self, k, v)
    
        def allocate(self, quantity):
            pass
    
        def is_allocation_consumption_possible(self, quantity):
            return True
    
        def consume_allocation(self, quantity):
            pass
        
        def cancel_allocation(self, quantity):
            pass
        
        @property
        def net_stock_level(self):
            return 0
    
        def set_discount_price(self, price):
            """
            A setter method for setting a new price.
    
            This is called from within the "discount" app, which is responsible
            for applying fixed-discount offers to products.  We use a setter method
            so that this behaviour can be customised in projects.
            """
            self.product.price_excl_tax = price
            self.product.save()
    
        @property
        def is_available_to_buy(self):
            """
            Return whether this stockrecord allows the product to be purchased
            """
            return True
    
        def is_purchase_permitted(self, user=None, quantity=1):
            """
            Return whether this stockrecord allows the product to be purchased by a
            specific user and quantity
            """
            return True, None
    
        @property
        def is_below_threshold(self):
            return False
    
        @property
        def availability_code(self):
            """
            Return an product's availability as a code for use in CSS to add icons
            to the overall availability mark-up.  For example, "instock",
            "unavailable".
            """
            return 'instock'
    
        @property
        def availability(self):
            """
            Return a product's availability as a string that can be displayed to the
            user.  For example, "In stock", "Unavailable".
            """
            return "In stock"
    
        def max_purchase_quantity(self, user=None):
            """
            Return an item's availability as a string
    
            :param user: (optional) The user who wants to purchase
            """
            return 9999
    
        @property
        def dispatch_date(self):
            """
            Return the estimated dispatch date for a line
            """
            return None
    
        @property
        def lead_time(self):
            return None
    
        @property
        def price_incl_tax(self):
            """
            Return a product's price including tax.
    
            This defaults to the price_excl_tax as tax calculations are
            domain specific.  This class needs to be subclassed and tax logic
            added to this method.
            """
            if self.price_excl_tax is None:
                return D('0.00')
            return self.price_excl_tax + self.price_tax
    
        @property
        def price_tax(self):
            """
            Return a product's tax value
            """
            return D('0.00')
    
        def __unicode__(self):
            return self.product.title
        
        # these methods simulate basic model functionality    
        def delete(self):
            return
        
        def save(self):
            raise TypeError('Stock records are disabled and cannot be saved')
        
        def get_query_set(self, **db_hints):
            raise TypeError('Stock records are disabled.')
    
        def get_prefetch_query_set(self, instances):
            raise TypeError('Stock records are disabled and cannot be prefetched.')
    
        def is_cached(self, instance):
            raise TypeError('Stock records are disabled and cannot be prefetched.')    
  
    
# this must remain at the bottom of this file - comment out before doing auto import    
from oscar.apps.catalogue.models import *  # @UnusedWildImport
