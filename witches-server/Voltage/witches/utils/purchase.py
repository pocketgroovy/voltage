from base64 import b64decode
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from witches import const
from witches.utils.custom_exceptions import ReceiptVerificationError
import urllib2
import json

from Voltage.settings import SANDBOX_URL_APPLE, LIVE_URL_APPLE, AMAZON_URL
import logging


logger = logging.getLogger(__name__)


def verify_apple_receipt(receipt_data):
    data = {"receipt-data": receipt_data}
    headers = {'Content-Type': 'text/Json; charset=utf-8'}
    dataj = json.dumps(data)

    # try production
    response_json = post_to_apple_store_verfication(LIVE_URL_APPLE, dataj, headers)

    # if failure, try sandbox
    if response_json['status'] == const.sandbox_receipt:
        response_json = post_to_apple_store_verfication(SANDBOX_URL_APPLE, dataj, headers)

    if response_json['status'] != const.receipt_verified:
        raise ReceiptVerificationError('failed ios receipt verification')

    return response_json


def post_to_apple_store_verfication(url, data, headers):
        request_to_send = urllib2.Request(url=url, data=data, headers=headers)
        # getting the response
        response = urllib2.urlopen(request_to_send)
        response_json = json.loads(response.read())
        return response_json


def verify_amazon_receipt(receipt_data):
    receipt = json.loads(receipt_data)
    amazon_user_id = receipt['amazon_user_id']
    receipt_id = receipt['receipt_id']

    URL = '{AMAZON_URL}/user/{amazon_user_id}/receiptId/{receipt_id}'.format(AMAZON_URL=AMAZON_URL,
                                                                             amazon_user_id=amazon_user_id,
                                                                             receipt_id=receipt_id)
    headers = {'Content-Type': 'text/Json; charset=utf-8'}

    request_to_send = urllib2.Request(url=URL, headers=headers)

    response = try_amazon_receipt_verification(request_to_send)  # if 500 returns, try 3 times.

    response_json = json.loads(response.read())

    return response_json, amazon_user_id


number_of_retry = 3
internal_server_error = 500
def try_amazon_receipt_verification(request_to_send):
    i = 0
    while i < number_of_retry:
        try:
            response = urllib2.urlopen(request_to_send)
            return response
        except urllib2.HTTPError as e:
            if e.code == internal_server_error:
                i += 1
            else:
                raise
    raise ReceiptVerificationError('Amazon receipt verification HTTP Error 500')


def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]


def pem_format(key):
    return '\n'.join([
        '-----BEGIN PUBLIC KEY-----',
        '\n'.join(chunks(key, 64)),
        '-----END PUBLIC KEY-----'
    ])


#  public key from Google developer console
const.android_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlA1mnAkRlKAOjhe238V0GD8buk1u2eTB1Ew2qAn/WI57oyFjw5cV6Qh5Wh8PH38/wV62NFfVp071NR8Wm2yhPwXzse3DLUdqPW4FKxNhRzck6q12MnSmUergqh2qflB/hkMOLj8mn5nix0xYcbyq0/PYjDVNccPZnLEaJpmYdcKWO5V7cNH6wB+bzkFKbAFqEmZtNAEkSYaW7ZNoJzhKQZjfB1xdgKN7x2DDgvcL6p12fdbx9M2pEvzyJZAqJ7tMWlgeptGqIO11MQUDx+wou1OVTczyscSxMqMjqG/HGT7gQtREsmJM3w0DrQeD8IuUS6eofuwExaUes+bM9+OazQIDAQAB'

#  refer to http://stackoverflow.com/questions/5440550/verifying-signature-on-android-in-app-purchase-message-in-python-on-google-app-e
def verify_android_receipt(receipt, signature):
    key = RSA.importKey(pem_format(const.android_key))
    verifier = PKCS1_v1_5.new(key)
    receipt_string = json.dumps(receipt)
    sanitized_for_verification = sanitize_receipt(receipt_string)
    receipt_data = SHA.new(sanitized_for_verification)
    sig = b64decode(signature)
    return verifier.verify(receipt_data, sig)

# "json.loads" inserts white spaces like {"orderId": "GPA.1313-2048-1054-43880",.. instead of {"orderId":"GPA.1313-2048-1054-43880",..
# this makes the verification fail so removing them.
def sanitize_receipt(receipt):
    sanitized_for_verification = receipt.translate(None, ' ')  # removing a white space
    return sanitized_for_verification