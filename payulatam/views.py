from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from payulatam.forms import PaymentNotificationForm


@method_decorator(csrf_exempt, name='dispatch')
class PaymentNotificationView(View):
    form_class = PaymentNotificationForm

    def post(self, request):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            return HttpResponse(status=200)
        print(form.errors)
        return HttpResponse(status=200)
