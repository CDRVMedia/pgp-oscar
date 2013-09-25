from oscar.apps.dashboard.catalogue.app import \
    CatalogueApplication as BaseCatalogueApplication
from pgp.shop.dashboard.catalogue.views import CategoryListView
from pgp.shop.dashboard.catalogue.views import ProductCreateUpdateView, \
    ProductListView, CategoryCreateView, CategoryUpdateView


class CatalogueApplication(BaseCatalogueApplication):
    category_create_view = CategoryCreateView
    category_update_view = CategoryUpdateView
    category_list_view = CategoryListView
    product_createupdate_view = ProductCreateUpdateView
    product_list_view = ProductListView

application = CatalogueApplication()
