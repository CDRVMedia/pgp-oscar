from django import forms
from django.db.models.loading import get_model
from django.forms.fields import CharField, DecimalField
from django.forms.models import ModelChoiceField
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from oscar.apps.dashboard.catalogue.forms import \
    CategoryForm as BaseCategoryForm, ProductForm as BaseProductForm, \
    ProductCategoryForm as BaseProductCategoryForm
from pgp import settings

ProductCategory = get_model('catalogue', 'ProductCategory')
Category = get_model('catalogue', 'Category')
Product = get_model('catalogue', 'Product')


class CategoryForm(BaseCategoryForm):
    additional_exclude = ['game']
        
    def __init__(self, *args, **kwargs):
        self.game = kwargs.pop('game', None) or kwargs['instance'].game  # we need the game to verify slug-game uniqueness in the form
        super(CategoryForm, self).__init__(*args, **kwargs)   
        # run through the related_to choices to eliminate categories that don't belong to self.game
        choices = []
        for pk, text in self.declared_fields['_ref_node_id'].choices:
            if pk is not 0:  # 0 is reserved for --root--
                try:
                    Category.objects.get(pk=pk, game=self.game)
                except Category.DoesNotExist:
                    # not found so this category doesn't belong to self.game, move to next choice
                    continue
            choices.append((pk, text))
        self.fields['_ref_node_id'].choices = choices
        # kill our additional exclude fields
        for field in self.additional_exclude:
            self.fields.pop(field)
            
    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        # make sure _ref_node_id refers to a node that's owned by self.game 
        if cleaned_data['_ref_node_id'] is not 0:
            try:
                Category.objects.get(pk=cleaned_data['_ref_node_id'],
                                     game=self.game)
            except Category.DoesNotExist:
                # this is not good - maybe it was tampered with.  Just make this a root node
                cleaned_data['_ref_node_id'] = 0
                
        # ensure game-slug uniqueness
        name = cleaned_data.get('name')
        ref_node_pk = cleaned_data.get('_ref_node_id')
        pos = cleaned_data.get('_position')

        slug = self.generate_slug(name, ref_node_pk, pos)

        try:
            category = Category.objects.get(game=self.game,
                                            slug=slug)
        except Category.DoesNotExist:
            pass
        else:
            if category.pk != self.instance.pk:
                raise forms.ValidationError(_('Category with the given path'
                                              ' already exists.'))
        return cleaned_data            
    
    def generate_slug(self, name, ref_node_pk, position):
        # determine parent
        if ref_node_pk:
            ref_category = Category.objects.get(pk=ref_node_pk)
            if position == 'first-child':
                parent = ref_category
            else:
                parent = ref_category.get_parent()
        else:
            parent = None

        # build full slug
        slug_prefix = (parent.slug + Category._slug_separator) if parent else ''
        slug = '%s%s' % (slug_prefix, slugify(name))
        return slug        

    def is_slug_conflicting(self, name, ref_node_pk, position):
        # handles slug uniqueness now handled in clean
        return False

class ProductForm(BaseProductForm):
    title = CharField(label=_('Title'), required=True, max_length=255)
    price_excl_tax = DecimalField(label=_('Price') + ' (%s)' % settings.OSCAR_DEFAULT_CURRENCY,
                                  required=True, decimal_places=2, max_digits=12)

    class Meta:
        model = Product
        fields = ['title',
                  'description',
                  # 'parent',    may be added back in later
                  # 'related_products',  may be added back in later
                  'price_excl_tax']
                   
        
    def __init__(self, product_class, *args, **kwargs):
        self.product_class = product_class
        self.set_initial_attribute_values(kwargs)
        super(BaseProductForm, self).__init__(*args, **kwargs)  # super to BaseForm because this replaces BaseForm's init
        self.add_attribute_fields()
        # PGP dropping related products and parent from init - see base form for original init
        
    def clean(self):
        return super(BaseProductForm, self).clean()  # skip BaseForm clean since it deals with parent issues        

def product_category_form_factory(game):
    '''
    The ProductCateogryForm Class is created with this 
    factory in order to allow the view to pass request.game
    into the form.  ProductCategoryForm is used in a formset
    which is not accommodating when it comes to passing in kwargs
    This version of ProductCategoryForm filters the category queryset
    to the specified game
    '''
    class ProductCategoryForm(BaseProductCategoryForm):
        category = ModelChoiceField(queryset=Category.objects.filter(game=game))
    
    return ProductCategoryForm


class ProductSearchForm(forms.Form):
    # PGP: override to hide the upc field since we are not using upcs
    upc = forms.CharField(max_length=16, required=False, label=_('UPC'), widget=forms.HiddenInput())
    title = forms.CharField(max_length=255, required=False, label=_('Title'))
