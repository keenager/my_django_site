from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import config.settings
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery
from public_def.functions.get_data import getData, LoginError
from public_def.functions.insert_schedule import insert_event
import os
import requests
from requests import Response
import json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# Create your views here.

# 참조: https://developers.google.com/identity/protocols/oauth2/web-server?hl=ko#example

CLIENT_SECRETS_FILE = f"{config.settings.BASE_DIR}/public_def/credentials.json"
REDIRECT_URL = 'http://localhost:8000/public_def/oauth2callback' if config.settings.DEBUG == True else 'https://public-def.fly.dev/public_def/oauth2callback'
SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

HOW_MANY_WEEKS = 5


def index(request):
    return render(request, 'public_def/index.html')


def api_request(request: HttpRequest):
    if 'access_token' not in request.session:
        return redirect('public_def:authorize')

    credentials = google.oauth2.credentials.Credentials(
        # **json.loads(request.session['credentials'])
        token=request.session['access_token']
    )
    calendar = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    # try:
    # schedule = getData(
    #     request.POST.get('id'),
    #     request.POST.get('password'),
    #     HOW_MANY_WEEKS
    # )
    data = {
        'id': request.POST.get('id'),
        'password': request.POST.get('password'),
    }
    res: Response = requests.post(
        'http://34.168.107.100:8000/get_data', data=data)

    try:
        schedules = json.loads(res.text)
        insert_event(calendar, schedules)
    except Exception:
        print(f'res: {res}')
        return render(request, 'public_def/index.html', {'message': res.text})
    else:
        return redirect('public_def:result')


def authorize(request: HttpRequest):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URL

    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')

    request.session['state'] = state

    print("request.session['state']: " + request.session['state'])

    return redirect(authorization_url)


def oauth2callback(request: HttpRequest):
    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URL
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    request.session['access_token'] = credentials.token

    return redirect('public_def:api_request')


def result(request):

    return render(request, 'public_def/result.html')


# def google_login(request):
#     client_id = ''
#     client_secret = ''

#     scope = 'https://www.googleapis.com/auth/calendar'
#     redirect_uri = 'http://localhost:8000/public_def/google_login/callback'
#     google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"
#     return redirect(f'{google_auth_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}')


# def google_login_callback(request):
#     code = request.GET.get('code')
#     google_token_api = "https://oauth2.googleapis.com/token"
#     access_token = get_access_token(google_token_api, code)
#     print(f'access_token -----> {access_token}')
#     insert_event(access_token)
#     return redirect('public_def:result')


# def get_access_token(google_token_api, code):
#     client_id = ""
#     client_secret = ""
#     code = code
#     grant_type = 'authorization_code'
#     redirection_uri = 'http://localhost:8000/public_def/google_login/callback'
#     state = "374tywvnovn7t89"

#     google_token_api += \
#         f"?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={redirection_uri}&state={state}"

#     token_response = requests.post(google_token_api)
#     pprint(f'token_response ---> {token_response.json()}')
#     if not token_response.ok:
#         raise ValidationError('Google token is invalid.')

#     access_token = token_response.json().get('access_token')

#     return access_token
