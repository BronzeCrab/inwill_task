from django.views.generic.edit import FormView
from django.contrib import messages
from .models import Account, BallanceHistory
from .form import BallanceChangeForm

from datetime import datetime


class BallanceChangeView(FormView):
    template_name = 'ballance_change.html'
    form_class = BallanceChangeForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(BallanceChangeView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.all()
        return context

    def form_valid(self, form):
        acc_qs = Account.objects.filter(id=1)
        ballance_change = form.cleaned_data.get('ballance_change')
        if ballance_change == 0:
            messages.add_message(
                self.request, messages.INFO, "Error cant change ballance by 0")
            return super().form_valid(form)
        if not acc_qs:
            acc = Account(ballance=ballance_change)
            acc.save()
            b_h = BallanceHistory(
                ballance_change=ballance_change,
                timestamp=datetime.now(), account=acc)
            b_h.save()
        else:
            acc = acc_qs[0]
            messages.add_message(
                self.request, messages.INFO,
                acc.change_ballance(ballance_change))
        return super().form_valid(form)
