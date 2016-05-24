from django.db import models
from VoltageSales.settings import MEDIA_ROOT


class Loadfile(models.Model):
    filePath = models.FileField(upload_to=MEDIA_ROOT)
    fileType = models.CharField(max_length=10)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Loadfile"


class AppleSales(models.Model):
    provider = models.CharField(max_length=50)
    providerCountry = models.CharField(max_length=10)
    sku = models.CharField(max_length=30)
    developer = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    version = models.DecimalField(max_digits=15, decimal_places=2)
    productTypeIdentifier = models.CharField(max_length=10)
    units = models.CharField(max_length=10)
    developerProceeds = models.CharField(max_length=10)
    beginDate = models.DateField()
    endDate = models.DateField()
    customerCurrency = models.CharField(max_length=5)
    countryCode = models.CharField(max_length=5)
    currencyOfProceeds = models.CharField(max_length=5)
    appleIdentifier = models.CharField(max_length=30)
    customerPrice = models.CharField(max_length=15)
    promoCode = models.CharField(max_length=30)
    parentIdentifier = models.CharField(max_length=30)
    subscription = models.CharField(max_length=50)
    period = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "AppleSales"


class GoogleSales(models.Model):
    orderNumber = models.CharField(max_length=50)
    orderChangedDate = models.DateField()
    orderChangedTimestamp = models.CharField(max_length=15)
    financialStatus = models.CharField(max_length=30)
    deviceModel = models.CharField(max_length=30)
    productTitle = models.CharField(max_length=100)
    productID = models.CharField(max_length=50)
    productType = models.CharField(max_length=30)
    skuID = models.CharField(max_length=50)
    currencyOfSale = models.CharField(max_length=20)
    itemPrice = models.CharField(max_length=15)
    taxesCollected = models.CharField(max_length=15)
    chargedAmount = models.CharField(max_length=15)
    cityOfBuyer = models.CharField(max_length=50)
    stateOfBuyer = models.CharField(max_length=30)
    zipOfBuyer = models.CharField(max_length=10)
    countryOfBuyer = models.CharField(max_length=5)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "GoogleSales"