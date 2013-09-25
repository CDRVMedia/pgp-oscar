from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from oscar.apps.dashboard.app import \
    DashboardApplication as BaseDashboardApplication
from pgp.shop.dashboard.catalogue.app import application as catalogue_app
from pgp.shop.dashboard.express.app import application as express_app
from pgp.shop.dashboard.orders.app import application as orders_app
from pgp.shop.dashboard.reports.app import application as reports_app
from pgp.shop.dashboard.views import IndexView



class DashboardApplication(BaseDashboardApplication):
    catalogue_app = catalogue_app
    orders_app = orders_app
    reports_app = reports_app
    express_app = express_app
    # views
    index_view = IndexView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.index_view.as_view(), name='index'),
            url(r'^catalogue/', include(self.catalogue_app.urls)),
            url(r'^reports/', include(self.reports_app.urls)),
            url(r'^orders/', include(self.orders_app.urls)),
            url(r'^express/', include(self.express_app.urls)),
            # url(r'^users/', include(self.users_app.urls)),
            # url(r'^content-blocks/', include(self.promotions_app.urls)),
            # url(r'^pages/', include(self.pages_app.urls)),
            # url(r'^offers/', include(self.offers_app.urls)),
            # url(r'^ranges/', include(self.ranges_app.urls)),
            # url(r'^reviews/', include(self.reviews_app.urls)),
            # url(r'^vouchers/', include(self.vouchers_app.urls)),
            # url(r'^comms/', include(self.comms_app.urls)),
        )
        return self.post_process_urls(urlpatterns)

application = DashboardApplication()
