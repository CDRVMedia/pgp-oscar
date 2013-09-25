from django.http import Http404
from django.shortcuts import get_object_or_404
from oscar.apps.dashboard.orders.views import OrderListView as BaseOrderListView, \
    LineDetailView as BaseLineDetailView, OrderDetailView as BaseOrderDetailView, OrderStatsView as BaseOrderStatsView
from pgp.shop.dashboard.orders.forms import OrderSearchForm

class LineDetailView(BaseLineDetailView):

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(pk=self.kwargs['line_id'],
                                          order__developer=self.request.developer)
        except self.model.DoesNotExist:
            raise Http404()


class OrderDetailView(BaseOrderDetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, 
                                 number=self.kwargs['number'],
                                 developer=self.request.developer)        


class OrderListView(BaseOrderListView):
    form_class = OrderSearchForm
    
    def get_queryset(self):
        return super(OrderListView, self).get_queryset().filter(developer=self.request.developer)
    
    
class OrderStatsView(BaseOrderStatsView):

    def get_context_data(self, **kwargs):
        ctx = super(BaseOrderStatsView, self).get_context_data(**kwargs)
        filters = kwargs.get('filters', {'developer':self.request.developer})
        ctx.update(self.get_stats(filters))
        ctx['title'] = kwargs['form'].get_filter_description()
        return ctx    