from oscar.apps.dashboard.orders.forms import OrderSearchForm as BaseOrderSearchForm

class OrderSearchForm(BaseOrderSearchForm):
    exclude_fields = ['upc', 'partner_sku']

    def __init__(self, *args, **kwargs):
        super(OrderSearchForm, self).__init__(*args, **kwargs)
        for field in self.exclude_fields:
            del self.fields[field]
        
