import logging
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import const
from utils.date_util import get_utc_datetime_by_adding_7hrs_to_pt, get_start_end_of_month_from_str
from witcheskpi.data import get_weekly_results, get_monthly_results

logger = logging.getLogger(__name__)

const.all = 0
const.apple = 1
const.google = 2
const.amazon = 3
const.leap_year_feb_end = 29
const.stone_quintet = 'com.voltage.ent.witch.001'
const.stone_cache = 'com.voltage.ent.witch.002'
const.stone_assembly = 'com.voltage.ent.witch.003'
const.stone_chest = 'com.voltage.ent.witch.004' # used to be satchel
const.stone_hoard = 'com.voltage.ent.witch.005'
const.stone_constel = 'com.voltage.ent.witch.006'
const.stamina_batch = 'com.voltage.ent.witch.101'
const.stamina_set = 'com.voltage.ent.witch.102'
const.stamina_case = 'com.voltage.ent.witch.103'
const.stamina_hoard = 'com.voltage.ent.witch.104'

const.last_month = 1
const.two_months_ago = 2
const.three_months_ago = 3
const.four_months_ago = 4
const.five_months_ago = 5
const.shop_type_apple = 'APPLE'
const.shop_type_google = 'GOOGLE'
const.shop_type_amazon = 'AMAZON'
const.shop_type_all = 'ALL'
const.device_type_apple = 'IPhonePlayer'
const.device_type_ggl = 'Android'
const.device_type_amazon = 'Amazon'
const.device_type_all = 'ALL'


@csrf_exempt
def home(request):
    context = RequestContext(request)
    return render_to_response('index.html', context_instance=context)


@csrf_exempt
def kpi(request):
    context = RequestContext(request)
    state = ''

    if request.POST:
        selected_month = request.POST.get('startDate')

        if not selected_month:
            state = 'Please select the Month you want to see!'
            return render_to_response('results.html', {'state': state, 'resultsType': const.all}, context_instance=context)

        selected_start_date_in_pt, selected_end_month_in_pt = get_start_end_of_month_from_str(selected_month)

        selected_start_date_in_utc, selected_end_monthin_utc = get_utc_datetime_by_adding_7hrs_to_pt(selected_start_date_in_pt,
                                                                                                   selected_end_month_in_pt)
        selected_device = int(request.POST.get('selected_device'))

        if selected_device == const.apple:
            monthly_results = get_monthly_results(selected_start_date_in_utc, selected_end_monthin_utc, selected_month,
                                                  const.shop_type_apple)
            weekly = get_weekly_results(selected_start_date_in_utc, const.shop_type_apple)

        elif selected_device == const.google:
            monthly_results = get_monthly_results(selected_start_date_in_utc, selected_end_monthin_utc, selected_month,
                                                  const.shop_type_google)
            weekly = get_weekly_results(selected_start_date_in_utc, const.shop_type_google)

        elif selected_device == const.amazon:
            monthly_results = get_monthly_results(selected_start_date_in_utc, selected_end_monthin_utc, selected_month,
                                                  const.shop_type_amazon)
            weekly = get_weekly_results(selected_start_date_in_utc, const.shop_type_amazon)

        elif selected_device == const.all:
            monthly_results = get_monthly_results(selected_start_date_in_utc, selected_end_monthin_utc, selected_month,
                                                  const.shop_type_all)
            weekly = get_weekly_results(selected_start_date_in_utc, const.shop_type_all)

        base_fields = {'resultsType': selected_device, 'startDate': selected_month, 'daily_results': weekly}
        response = dict(base_fields, **monthly_results)

        return render_to_response('results.html', response, context_instance=context)

    else:
        return render_to_response('results.html', {'state': state, 'resultsType': const.all}, context_instance=context)

