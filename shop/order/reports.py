import datetime
from django.db.models.loading import get_model
from oscar.apps.order.reports import OrderReportGenerator as BaseOrderReportGenerator

Order = get_model('order','Order')

class OrderReportGenerator(BaseOrderReportGenerator):

    def generate(self):
        orders = Order._default_manager.filter(
            date_placed__gte=self.start_date,
            date_placed__lt=self.end_date + datetime.timedelta(days=1),
            developer=self.developer
        )

        additional_data = {
            'start_date': self.start_date,
            'end_date': self.end_date
        }

        return self.formatter.generate_response(orders, **additional_data)

    def is_available_to(self, user):
        return user.is_staff