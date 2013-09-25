from oscar.apps.dashboard.reports.reports import ReportGenerator as BaseReportGenerator

class ReportGenerator(BaseReportGenerator):
    """
    Override ReportGenerator to require the developer
    """

    def __init__(self, **kwargs):
        self.developer = kwargs.pop('developer')
        super(ReportGenerator, self).__init__(**kwargs)
