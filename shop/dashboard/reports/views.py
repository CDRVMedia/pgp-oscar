from django.http import Http404
from oscar.apps.dashboard.reports.views import IndexView as BaseIndexView


class IndexView(BaseIndexView):

    def _get_generator(self, form):
        ''' override to pass in request.developer '''
        code = form.cleaned_data['report_type']

        repo = self.generator_repository()
        generator_cls = repo.get_generator(code)
        if not generator_cls:
            raise Http404()

        download = form.cleaned_data['download']
        formatter = 'CSV' if download else 'HTML'

        return generator_cls(start_date=form.cleaned_data['date_from'],
                             end_date=form.cleaned_data['date_to'],
                             developer=self.request.developer,
                             formatter=formatter)