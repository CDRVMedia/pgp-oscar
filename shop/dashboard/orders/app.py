from oscar.apps.dashboard.orders.app import \
    OrdersDashboardApplication as BaseOrdersDashboardApplication
from pgp.shop.dashboard.orders.views import OrderListView, LineDetailView, \
    OrderDetailView, OrderStatsView


class OrdersDashboardApplication(BaseOrdersDashboardApplication):
    line_detail_view = LineDetailView
    order_list_view = OrderListView
    order_detail_view = OrderDetailView
    order_stats_view = OrderStatsView

application = OrdersDashboardApplication()
