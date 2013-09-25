from django.db.models.loading import get_model
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from oscar.apps.dashboard.catalogue.forms import BaseProductCategoryFormSet
from oscar.apps.dashboard.catalogue.views import \
    CategoryDeleteView as BaseCategoryDeleteView, \
    CategoryListView as BaseCategoryListView, \
    CategoryCreateView as BaseCategoryCreateView, \
    ProductListView as BaseProductListView, \
    ProductCreateUpdateView as BaseProductCreateUpdateView, \
    CategoryUpdateView as BaseCategoryUpdateView
from pgp.shop.dashboard.catalogue.forms import ProductForm, ProductSearchForm, \
    CategoryForm, product_category_form_factory
from pgp.shop.dashboard.catalogue.mixins import CategoryViewMixin

Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')
ProductCategory = get_model('catalogue', 'ProductCategory')

class CategoryCreateView(BaseCategoryCreateView):
    form_class = CategoryForm
    
    def form_valid(self, form):
        # insert game into cleaned data so game is populated in the model instance
        form.cleaned_data['game'] = self.request.game
        return super(CategoryCreateView, self).form_valid(form) 
    
    def get_form_kwargs(self):
        kwargs = super(CategoryCreateView, self).get_form_kwargs()
        kwargs['game'] = self.request.game
        return kwargs
    
class CategoryDeleteView(CategoryViewMixin, BaseCategoryDeleteView):
    pass
    

class CategoryListView(BaseCategoryListView):

    def get_context_data(self, *args, **kwargs):
        '''
        filter categories to include only categories belonging to current game
        '''
        ctx = super(CategoryListView, self).get_context_data(*args, **kwargs)
        ctx['child_categories'] = ctx['child_categories'].filter(game=self.request.game)
        return ctx    



    
class CategoryUpdateView(CategoryViewMixin, BaseCategoryUpdateView):
    form_class = CategoryForm    


class ProductCreateUpdateView(BaseProductCreateUpdateView):
    form_class = ProductForm
    
    def dispatch(self, request, *args, **kwargs):
        # set the formset class using our form_factory to pass request.game to the actual form
        self.category_formset = inlineformset_factory(
            Product, ProductCategory,
            form=product_category_form_factory(request.game),
            formset=BaseProductCategoryFormSet,
            fields=('category',),
            extra=1,
            can_delete=False)
        return super(ProductCreateUpdateView, self).dispatch(request, *args, **kwargs) 

    def is_stockrecord_submitted(self):
        """
        PGP - Setting this to False since we are not using StockRecords
        """
        return False
    
    def form_valid(self, form):
        # add partner into the instance since this field is required in the model but not present in the form
        form.instance.partner = self.request.game.partner
        return super(ProductCreateUpdateView, self).form_valid(form)    
    
    def get_stockrecord_form(self):
        return None 
    
    def get_queryset(self):
        return super(ProductCreateUpdateView, self).get_queryset().filter(partner__game=self.request.game)     

class ProductListView(BaseProductListView):
    form_class = ProductSearchForm
    
    def get_queryset(self):
        """
        Build the queryset for this list and also update the title that
        describes the queryset
        PGP: Same as base but removes stockrecord prefetch
        """
        description_ctx = {'upc_filter': '',
                           'title_filter': ''}
        queryset = self.model.objects.filter(partner__game=self.request.game).order_by('-date_created').prefetch_related(
            'product_class')
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            self.description = self.description_template % description_ctx
            return queryset

        data = self.form.cleaned_data

        if data['upc']:
            queryset = queryset.filter(upc=data['upc'])
            description_ctx['upc_filter'] = _(" including an item with UPC '%s'") % data['upc']

        if data['title']:
            queryset = queryset.filter(title__icontains=data['title']).distinct()
            description_ctx['title_filter'] = _(" including an item with title matching '%s'") % data['title']

        self.description = self.description_template % description_ctx
        return queryset
    
