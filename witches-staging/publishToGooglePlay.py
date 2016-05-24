#!/usr/bin/env python

# https://developers.google.com/api-client-library/python/auth/service-accounts
# https://developers.google.com/analytics/devguides/reporting/core/v2/gdataAuthentication
# https://google-api-python-client.googlecode.com/hg/docs/epy/apiclient-module.html
# pip install --upgrade google-api-python-client
# pip install PyOpenSSL
# pip install pycrypto
# openssl pkcs12 -in Google\ Play\ Android\ Developer-33183780f00d.p12 -nodes -nocerts > key.pem
# openssl pkcs8 -nocrypt -in key.pem -passin pass:notasecret -topk8 -out privatekey.pem


import sys
import argparse
import os.path

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client import client 
from httplib2 import Http



DEFAULT_TRACK = 'alpha'          # 'alpha', beta', 'production', 'rollout'

SCOPE = 'https://www.googleapis.com/auth/androidpublisher'
SERVICE_EMAIL = '930440757754-eb41a3p76g9vp062u8us26d5gfibv2pu@developer.gserviceaccount.com'
KEY_PATH = 'Certificates/Android/Google Play Android Developer-33183780f00d.pem'     



def commit_edit(service, edit_id, package_name):
    commit_response = service.edits().commit(editId=edit_id, packageName=package_name).execute()

    if ('id' in commit_response):
        print "Edit '{0}' Committed".format (commit_response['id'])
    else:
        raise Exception("Commit '{0}' Failed".format(edit_id))


# def validate_edit(service, edit_id, package_name):
    # validate_response = service.edits().validate(editId=edit_id, packageName=package_name).execute()


def set_description(service, edit_id, package_name, version_code, changelog):
    listing_response = service.edits().apklistings().update(editId=edit_id, packageName=package_name, language='en-US', apkVersionCode=version_code, body={'recentChanges': changelog}).execute()

    print "Description for [{0}] Updated To: {1}".format(listing_response['language'], listing_response['recentChanges'])


def set_track(service, edit_id, package_name, version_code, track):
    track_response = service.edits().tracks().update(editId=edit_id, track=track, packageName=package_name, body={u'versionCodes': [version_code]}).execute()

    print "'{0} {1}' is set to track '{2}'".format (package_name, str(track_response['versionCodes']), track_response['track'])


def upload_apk(service, edit_id, package_name, apk_path, obb_path=None):

    print "Uploading APK: {0} OBB: {1}".format(apk_path, obb_path)

    # googleapiclient.errors.HttpError if version code exists or using different certificate
    apk = get_media_body(apk_path)
    apk_response = service.edits().apks().upload(editId=edit_id, packageName=package_name, media_body=apk).execute()

    version_code = apk_response['versionCode']
    print "APK Version Code: {0}".format (version_code)

    if(obb_path):
        obb = get_media_body(obb_path)
        obb_response = service.edits().expansionfiles().upload(editId=edit_id, packageName=package_name, apkVersionCode=version_code, expansionFileType='main', media_body=obb).execute()

        print "Expansion Uploaded: {0} bytes".format (obb_response['expansionFile']['fileSize'])

    return version_code

def get_media_body(path):
    if(valid_file(path)):
        return MediaFileUpload(path, mimetype='application/octet-stream', chunksize=1024*1024*3, resumable=True)    # is this request resumable?   
    else:
        raise Exception("File does not exist at path: {0}".format(path))

def valid_file(path):
    return os.path.isfile(path) 


def create_new_edit(service, package_name):
    edit_request = service.edits().insert(body={}, packageName=package_name)
    edit = edit_request.execute()

    print "New Edit '{0}' [{1}]".format (edit['id'], package_name)
    return edit


def create_publisher_service(client_email, key_path, scope):
    private_key = read_file(key_path)

    credentials = client.SignedJwtAssertionCredentials(client_email, private_key, scope, sub='google_play@voltage-ent.com')
    http_auth = credentials.authorize(Http())

    service = build('androidpublisher', 'v2', http=http_auth) #, cache_discovery=False)

    print ("Publisher Service Created: '{0}'").format(scope)
    return service


def read_file(path):
    with open(path, 'r') as file:   # can raise exception if file does not exist
        return file.read()


def GetArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('package_name', help="Package Name in reverse domain format (e.g., com.company.app)")
    # parser.add_argument('client_email', help="The service account 'client_email' provided by Google")
    # parser.add_argument('key_path', help="Path to P12 key (Note: JSON key won't work)")
    parser.add_argument('apk_path', help="Path to APK file (Requires a prior manual upload thru console)")
    parser.add_argument('--main', default=None, help="Path to OBB file (Requires a prior manual upload thru console)")        # parser.add_argument('obb_path', help="Path to OBB file")
    # parser.add_argument('changelog_path', help="Path to changelog file")
    parser.add_argument('--track', default=DEFAULT_TRACK, choices=['alpha', 'beta', 'production', 'rollout'])
    return parser.parse_args()


def main(argv):

    args = GetArguments()

    package_name = args.package_name 
    track = args.track
    client_email = SERVICE_EMAIL    # args.client_email
    key_path = KEY_PATH             # args.key_path
    apk_path = args.apk_path
    obb_path = args.main
    changelog = "staging build"     # read_file(args.changelog_path)

    try:
        # TODO: could encapsulate all of this in a custom Edit class/object in the future...
        service = create_publisher_service(client_email, key_path, SCOPE)
        edit = create_new_edit (service, package_name)

        edit_id = edit['id']

        version_code = upload_apk(service, edit_id, package_name, apk_path, obb_path)
        set_description(service, edit_id, package_name, version_code, changelog)
        set_track(service, edit_id, package_name, version_code, track)

        # validate_edit(service, edit_id, package_name)
        commit_edit(service, edit_id, package_name)

    except client.AccessTokenRefreshError:
        raise Exception("The credentials have been revoked/expired, rerun again")



if __name__ == '__main__':
    main(sys.argv)