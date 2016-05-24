
import json

import logging
logger = logging.getLogger(__name__)

from witches.models import ErrorLog, PaymentHistoryError

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def receive_error_report(request):

    ErrorLog.objects.create( 
        phone_id=request.POST.get('phone_id', default=''), 
        build_version=request.POST.get('build_version', default=''),
        playerjson=request.POST.get('playerjson', default=''), 
        error_msg=request.POST.get('error_msg', default=''), 
        stacktrace=request.POST.get('stacktrace', default=''),
        device_id=request.POST.get('device_id', default=''),
        device_model=request.POST.get('device_model', default=''),
        device_os=request.POST.get('device_os', default=''),
        device_system_mem=request.POST.get('device_system_mem', default=0),
        device_graphics_mem=request.POST.get('device_graphics_mem', default=0),
        )
    
    # always return success
    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type='application/json')


def payment_history_error(error,  phone_id, item_id, receipt, device_os):
    PaymentHistoryError.objects.create(
        error_message=error,
        phone_id=phone_id,
        item_id=item_id,
        receipt=receipt,
        device_os=device_os
    )
