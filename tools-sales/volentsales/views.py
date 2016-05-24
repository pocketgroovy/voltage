# Create your views here.

from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from django.db import transaction
from models import Loadfile, AppleSales, GoogleSales
from datetime import datetime

import zipfile
import os
import gzip
import csv


def index(request):
    context = RequestContext(request)
    return render_to_response('login.html', context_instance=context)


def home(request):
    context = RequestContext(request)

    user = request.user
    if user.is_authenticated():
        return render_to_response('home.html', context_instance=context)
    else:
        return render_to_response('login.html', context_instance=context)


def login_user(request):
    state = "Log in:"
    next_page = 'home.html'
    username = password = ''

    context = RequestContext(request)

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    state = "Welcome to Voltage Entertainment Sales Tool."
                    return render_to_response('home.html', {'state': state}, context_instance=context)
                else:
                    state = 'User is inactive, please contact your system manager.'
                    return render_to_response('login.html', {'state': state}, context_instance=context)
            else:
                state = 'User is not registered in the Data Base, please contact your system manager.'
                return render_to_response('login.html', {'state': state}, context_instance=context)
        else:
            if not username:
                state = 'Username cannot be blank, please insert a username.'
                return render_to_response('login.html', {'state': state}, context_instance=context)
            elif not password:
                state = 'Password cannot be blank, please insert a password'
                return render_to_response('login.html', {'state': state}, context_instance=context)
    else:
        return render_to_response('login.html', context_instance=context)


def register(request):
    context = RequestContext(request)

    if request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        email = request.POST.get('email')

        try:
            user = User.objects.get(username=username)
            if user:
                state = "This username already exists in the DataBase"
                return render_to_response('newuser.html', {'state': state, 'username': username,
                                                           'first_name': first_name, 'last_name': last_name,
                                                           'email': email},
                                          context_instance=context)
        except User.DoesNotExist:
            if password == conf_password:
                with transaction.commit_on_success():
                    try:
                        User.objects.create(username=username,
                                            password=make_password(password),
                                            first_name=first_name,
                                            last_name=last_name,
                                            is_staff=False,
                                            is_active=True,
                                            is_superuser=False)
                    except Exception:
                        transaction.rollback()
                        state = 'There was an error, please try again!.'
                        return render_to_response('newuser.html', {'state': state, 'username': username,
                                                                   'first_name': first_name, 'last_name': last_name,
                                                                   'email': email},
                                                  context_instance=context)
                state = "User register successfully! "
                return render_to_response('newuser.html', {'state': state}, context_instance=context)

            else:
                state = 'Password and Confirmation Password are incorrect.'
                return render_to_response('newuser.html', {'state': state, 'username': username,
                                                           'first_name': first_name, 'last_name': last_name,
                                                           'email': email},
                                          context_instance=context)

    else:
        return render_to_response('newuser.html', context_instance=context)


def upload(request):
    context = RequestContext(request)
    state = ''

    if request.POST:
        if request.POST.get("fileType") == '0':
            data = Loadfile.objects.create(filePath=request.FILES.get('datafile'), fileType='Apple')
        elif request.POST.get("fileType") == '1':
            data = Loadfile.objects.create(filePath=request.FILES.get('datafile'), fileType='Google')

        if data.filePath.name.endswith(".zip"):
            ziplist = zipfile.ZipFile(data.filePath.name)
            dir, name = os.path.split(data.filePath.name)
            for f in ziplist.namelist():
                ziplist.extract(f, dir)
                if request.POST.get("fileType") == '0':
                    insert_apple_file(dir, f)
                elif request.POST.get("fileType") == '1':
                    insert_google_file(dir, f)

                os.remove(dir + '/' + f)

        elif data.filePath.name.endswith(".gz"):
            dir, name = os.path.split(data.filePath.name)
            if request.POST.get("fileType") == '0':
                insert_apple_file(dir, name)
            elif request.POST.get("fileType") == '1':
                insert_google_file(dir, name)


        os.remove(data.filePath.name)
        state = 'File uploaded successfully!.'

    return render_to_response('load.html', {'state': state}, context_instance=context)


def insert_apple_file(dir, txtfile):
        if txtfile.endswith(".gz"):
            f = gzip.open(dir + '/' + txtfile, 'rb').readlines()
        elif txtfile.endswith(".txt"):
            f = open(dir + '/' + txtfile, 'rb').readlines()
        f.pop(0)
        for row in f:
            reader = row.split('\t')
            rowlist = list(reader)

            AppleSales.objects.create(provider=rowlist[0],
                                      providerCountry=rowlist[1],
                                      sku=rowlist[2],
                                      developer=rowlist[3],
                                      title=rowlist[4],
                                      version=0 if rowlist[5].strip() == '' else rowlist[5],
                                      productTypeIdentifier=rowlist[6],
                                      units=0 if rowlist[7].strip() == '' else rowlist[7],
                                      developerProceeds=0 if rowlist[8].strip() == '' else rowlist[8],
                                      beginDate=datetime.strptime(rowlist[9], "%m/%d/%Y").date(),
                                      endDate=datetime.strptime(rowlist[10], "%m/%d/%Y").date(),
                                      customerCurrency=rowlist[11],
                                      countryCode=rowlist[12],
                                      currencyOfProceeds=rowlist[13],
                                      appleIdentifier=rowlist[14],
                                      customerPrice=0 if rowlist[15].strip() == '' else rowlist[15],
                                      promoCode=rowlist[16],
                                      parentIdentifier=rowlist[17],
                                      subscription=rowlist[18],
                                      period=rowlist[19],
                                      category=rowlist[20])


def insert_google_file(dir, txtfile):
        if txtfile.endswith(".csv"):
            readfile = open(dir + '/' + txtfile, 'rb')
            f = csv.reader(readfile)
            headers = f.next()
        for rowlist in f:

                GoogleSales.objects.create(orderNumber=rowlist[0],
                                           orderChangedDate=datetime.strptime(rowlist[1], "%Y-%m-%d").date(),
                                           orderChangedTimestamp=rowlist[2],
                                           financialStatus=rowlist[3],
                                           deviceModel=rowlist[4],
                                           productTitle=rowlist[5],
                                           productID=rowlist[6],
                                           productType=rowlist[7],
                                           skuID=rowlist[8],
                                           currencyOfSale=rowlist[9],
                                           itemPrice=rowlist[10],
                                           taxesCollected=rowlist[11],
                                           chargedAmount=rowlist[12],
                                           cityOfBuyer=rowlist[13],
                                           stateOfBuyer=rowlist[14],
                                           zipOfBuyer=rowlist[15],
                                           countryOfBuyer=rowlist[16])


def results(request):
    context = RequestContext(request)
    state = ''
    applelist = googlelist = []
    apple_titles = AppleSales.objects.filter(version__gt=0).values('title').distinct()
    google_titles = GoogleSales.objects.filter(financialStatus='Charged').values('productID').distinct()
    currencies = list(AppleSales.objects.all().values_list('customerCurrency', flat=True).distinct())
    ggl_currencies = list(GoogleSales.objects.all().values_list('currencyOfSale', flat=True).distinct())

    for currency in ggl_currencies:
        if currency not in currencies:
            currencies.append(currency)

    if request.POST:
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        sel_apple_title = request.POST.get('sel_apple_title')
        sel_google_title = request.POST.get('sel_google_title')
        sel_currency = request.POST.get('sel_currency')
        tableType = request.POST.get('tableType')

        if startDate == '':
            state = 'Start Date cannot be null, please insert a start date!.'
            return render_to_response('results.html', {'state': state, 'apple_titles': apple_titles,
                                                       'endDate': endDate, 'google_titles': google_titles,
                                                       'currencies': currencies,
                                                       'resultsType': 9,
                                                       'sel_apple_title': sel_apple_title,
                                                       'sel_google_title': sel_google_title},
                                      context_instance=context)
        if endDate == '':
            state = 'End Date cannot be null, please insert an end date!.'
            return render_to_response('results.html', {'state': state, 'apple_titles': apple_titles,
                                                       'startDate': startDate, 'google_titles': google_titles,
                                                       'currencies': currencies,
                                                       'resultsType': 9,
                                                       'sel_apple_title': sel_apple_title,
                                                       'sel_google_title': sel_google_title},
                                      context_instance=context)

        if sel_google_title == '' and sel_apple_title == '':
            state = 'Please select a tittle to search!'
            return render_to_response('results.html', {'state': state, 'apple_titles': apple_titles,
                                                       'startDate': startDate, 'endDate': endDate,
                                                       'google_titles': google_titles,
                                                       'resultsType': 9,
                                                       'currencies': currencies,
                                                       'sel_apple_title': sel_apple_title,
                                                       'sel_google_title': sel_google_title},
                                      context_instance=context)

        startDate = datetime.strptime(request.POST.get('startDate'), "%m/%d/%Y").date()
        endDate = datetime.strptime(request.POST.get('endDate'), "%m/%d/%Y").date()
        resultsType = int(request.POST.get('resultsType'))

        if sel_apple_title:
            parentIdentifier = AppleSales.objects.filter(title=sel_apple_title)[0].sku


        total_results_google = []
        total_results = []
        installs = 0
        updates = 0
        total_apple = 0
        total_google = 0
        if resultsType == 0 or resultsType == 9:    # Apple
            install_codes = ['1', '1F']
            update_codes = ['7', '7F']
            installs = AppleSales.objects.filter(beginDate__gte=startDate, endDate__lte=endDate,
                                                 productTypeIdentifier__in=install_codes).count()
            updates = AppleSales.objects.filter(beginDate__gte=startDate, endDate__lte=endDate,
                                                productTypeIdentifier__in=update_codes).count()
            if tableType == 'total':
                if parentIdentifier and sel_currency:
                    customerPrices = AppleSales.objects.filter(parentIdentifier=parentIdentifier,
                                                               currencyOfProceeds=sel_currency,
                                                               beginDate__gte=startDate,
                                                               endDate__lte=endDate).\
                        values_list('customerPrice', flat=True).order_by('customerPrice').distinct()

                    for price in customerPrices:
                        price_count = AppleSales.objects.filter(parentIdentifier=parentIdentifier,
                                                                currencyOfProceeds=sel_currency,
                                                                customerPrice=price,
                                                                beginDate__gte=startDate,
                                                                endDate__lte=endDate).aggregate(Sum('units'))
                        total_results.append({
                            "customerPrice": price,
                            "units": price_count['units__sum']
                        })
                        total_apple += price_count['units__sum']
                elif parentIdentifier and not sel_currency:
                    customerPrices = AppleSales.objects.filter(parentIdentifier=parentIdentifier,
                                                               beginDate__gte=startDate,
                                                               endDate__lte=endDate).\
                        values_list('customerPrice', 'currencyOfProceeds').order_by('customerPrice').distinct()

                    for price, currency in customerPrices:
                        price_count = AppleSales.objects.filter(parentIdentifier=parentIdentifier,
                                                                customerPrice=price,
                                                                beginDate__gte=startDate,
                                                                endDate__lte=endDate).aggregate(Sum('units'))
                        total_results.append({
                            "currency": currency,
                            "customerPrice": price,
                            "units": price_count['units__sum']
                        })
                        total_apple += price_count['units__sum']
            elif tableType == 'breakdown':
                if parentIdentifier and sel_currency:
                    titles = AppleSales.objects.filter(productTypeIdentifier='IA1', currencyOfProceeds=sel_currency,
                                                       parentIdentifier=parentIdentifier, beginDate__gte=startDate,
                                                       endDate__lte=endDate).\
                        values_list('title', 'sku').order_by('title').distinct()

                    for title, sku in titles:
                        title_count = AppleSales.objects.filter(title=title, currencyOfProceeds=sel_currency,
                                                                parentIdentifier=parentIdentifier,
                                                                beginDate__gte=startDate,
                                                                endDate__lte=endDate).aggregate(Sum('units'))
                        total_results.append({
                            "title": title,
                            "units": title_count['units__sum']
                        })
                        total_apple += title_count['units__sum']
                elif parentIdentifier and not sel_currency:
                    titles = AppleSales.objects.filter(productTypeIdentifier='IA1',
                                                       parentIdentifier=parentIdentifier, beginDate__gte=startDate,
                                                       endDate__lte=endDate).\
                        values_list('title', 'sku').order_by('title').distinct()

                    for title, sku in titles:
                        title_count = AppleSales.objects.filter(title=title,
                                                                parentIdentifier=parentIdentifier,
                                                                beginDate__gte=startDate,
                                                                endDate__lte=endDate).aggregate(Sum('units'))
                        total_results.append({
                            "sku": sku,
                            "title": title,
                            "units": title_count['units__sum']
                        })
                        total_apple += title_count['units__sum']
        if resultsType == 1 or resultsType == 9:  # Google
            if tableType == 'total':
                if sel_currency:
                    itemPrices =GoogleSales.objects.filter(currencyOfSale=sel_currency, productID=sel_google_title,
                                                           orderChangedDate__gte=startDate,
                                                           orderChangedDate__lte=endDate).\
                        values_list('itemPrice', flat=True).order_by('itemPrice').distinct()

                    for price in itemPrices:
                        price_count = GoogleSales.objects.filter(currencyOfSale=sel_currency,
                                                                 productID=sel_google_title, itemPrice=price,
                                                                 orderChangedDate__gte=startDate,
                                                                 orderChangedDate__lte=endDate).count()

                        total_results_google.append({
                            "customerPrice": price,
                            "units": price_count
                        })
                        total_google += price_count
                else:
                    itemPrices =GoogleSales.objects.filter(productID=sel_google_title,
                                                           orderChangedDate__gte=startDate,
                                                           orderChangedDate__lte=endDate).\
                        values_list('itemPrice', flat=True).order_by('itemPrice').distinct()

                    for price in itemPrices:
                        price_count = GoogleSales.objects.filter(productID=sel_google_title, itemPrice=price,
                                                                 orderChangedDate__gte=startDate,
                                                                 orderChangedDate__lte=endDate).count()

                        total_results_google.append({
                            "customerPrice": price,
                            "units": price_count
                        })
                        total_google += price_count
            elif tableType == 'breakdown':
                if sel_currency:
                    itemPrices = GoogleSales.objects.filter(currencyOfSale=sel_currency, productID=sel_google_title,
                                                            orderChangedDate__gte=startDate,
                                                            orderChangedDate__lte=endDate).\
                        values_list('productTitle').order_by('productTitle').distinct()

                    for title in itemPrices:
                        title_count = GoogleSales.objects.filter(currencyOfSale=sel_currency,
                                                                 productID=sel_google_title,
                                                                 productTitle=title,
                                                                 orderChangedDate__gte=startDate,
                                                                 orderChangedDate__lte=endDate).count()

                        total_results_google.append({
                            "title": title,
                            "units": title_count
                        })
                        total_google += title_count
                else:
                    itemPrices = GoogleSales.objects.filter(productID=sel_google_title,
                                                            orderChangedDate__gte=startDate,
                                                            orderChangedDate__lte=endDate).\
                        values_list('productTitle').order_by('productTitle').distinct()

                    for title in itemPrices:
                        title_count = GoogleSales.objects.filter(productID=sel_google_title,
                                                                 productTitle=title,
                                                                 orderChangedDate__gte=startDate,
                                                                 orderChangedDate__lte=endDate).count()

                        total_results_google.append({
                            "title": title,
                            "units": title_count
                        })
                        total_google += title_count

        return render_to_response('results.html', {'state': state, 'total_results_google': total_results_google,
                                                   'currencies': currencies, 'total_results': total_results,
                                                   'apple_titles': apple_titles, 'google_titles': google_titles,
                                                   'sel_currency': sel_currency, 'sel_apple_title': sel_apple_title,
                                                   'sel_google_title': sel_google_title,
                                                   'startDate': datetime.strftime(startDate, '%m/%d/%Y'),
                                                   'endDate': datetime.strftime(endDate, '%m/%d/%Y'),
                                                   'tableType': tableType, 'installs': installs, 'updates': updates,
                                                   'total_apple': total_apple, 'total_google': total_google,
                                                   'resultsType': resultsType}, context_instance=context)
    else:
        return render_to_response('results.html', {'state': state, 'apple_titles': apple_titles,
                                                   'currencies': currencies, 'resultsType': 9, 'tableType': 'total',
                                                   'google_titles': google_titles}, context_instance=context)