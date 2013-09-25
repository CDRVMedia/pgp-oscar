from oscar.apps.dashboard.reports.app import \
    ReportsApplication as BaseReportsApplication
from pgp.shop.dashboard.reports.views import IndexView


class ReportsApplication(BaseReportsApplication):
    index_view = IndexView


application = ReportsApplication()
