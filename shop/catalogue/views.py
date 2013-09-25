from django.db.models import get_model
from oscar.apps.catalogue.views import \
    ProductCategoryView as BaseProductCategoryView, \
    ProductListView as BaseProductListView

Product = get_model('catalogue', 'product')
Category = get_model('catalogue', 'category')
Partner = get_model('partner', 'partner')

def get_product_base_queryset():
    """
    Return ``QuerySet`` for product model with related
    content pre-loaded. The ``QuerySet`` returns unfiltered
    results for further filtering.
    """
    return Product.browsable.select_related(
            'product_class',
        ).prefetch_related(
            'reviews',
            'variants',
            'product_options',
            'product_class__options',
            'images',
        ).all()
        
class ProductCategoryView(BaseProductCategoryView):
    """
    Browse products in a given category
    """
    
    def get_queryset(self):
        return get_product_base_queryset().filter(
            categories__in=self.categories
        ).distinct()        

class ProductListView(BaseProductListView):
    """
    A list of products
    """
    def get_queryset(self):
        q = self.get_search_query()
        if q:
            # Send signal to record the view of this product
            self.search_signal.send(sender=self, query=q, user=self.request.user)
            qs = get_product_base_queryset().filter(title__icontains=q)
        else:
            qs = get_product_base_queryset()
        # filter the list to include products owned by request.game
        return qs.filter(partner=Partner.objects.get(game=self.request.game))