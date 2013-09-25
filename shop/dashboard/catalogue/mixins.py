class CategoryViewMixin(object):
    
    def get_queryset(self):
        """
        Restrict the queryset to this game's categories
        """
        return super(CategoryViewMixin, self).get_queryset().filter(game=self.request.game) 