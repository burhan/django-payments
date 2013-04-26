from .. import get_payment_model
from ..paypal import PaypalProvider
from django.http import HttpResponseForbidden
from .forms import PaymentForm

Payment = get_payment_model()


class PaypalCardProvider(PaypalProvider):
    '''
    paypal.com credit card payment provider
    '''
    def get_form(self, data=None, ordered_items=None):
        return PaymentForm(data, provider=self, payment=self.payment)

    def get_product_data(self, extra_data):
        data = self.get_transactions_data()
        year = extra_data['expiration'].year
        month = extra_data['expiration'].month
        data['payer'] = {
            'payment_method': 'credit_card',
            'funding_instruments': [{
                'credit_card': {
                    'number': extra_data['number'],
                    'type': extra_data['type'],
                    'expire_month': month,
                    'expire_year': year,
                    'cvv2': extra_data['cvv2']}}]}
        return data

    def process_data(self, request):
        return HttpResponseForbidden('FAILED')