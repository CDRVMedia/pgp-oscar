from oscar.apps.catalogue.app import \
    CatalogueApplication as BaseCatalogueApplication
from pgp.shop.catalogue.views import ProductListView, ProductCategoryView

class CatalogueApplication(BaseCatalogueApplication):
    index_view = ProductListView
    category_view = ProductCategoryView    

application = CatalogueApplication()