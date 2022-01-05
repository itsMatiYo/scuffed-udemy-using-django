"""helper fucntions for program related to auth models"""
import json

import jwt
import requests
from decouple import config
from django.core.exceptions import ObjectDoesNotExist
from jwt.exceptions import ExpiredSignatureError
from rest_framework import exceptions, status
from rest_framework.response import Response

from users.models import Adviser, Student, Teacher, Wallet

# ! Server Information :
HOST = config('HOST')
AUTH_SECRET_KEY = config('AUTH_SECRET_KEY')
BASE_AUTH = config('BASE_AUTH')
SERVICE_ID = config('SERVICE_ID')
ROLE_ID_TEACHER = config('ROLE_ID_TEACHER')
ROLE_ID_STUDENT = config('ROLE_ID_STUDENT')
ROLE_ID_ADVISER = config('ROLE_ID_ADVISER')


# todo : Get Wallet
def get_wallet(token):
    try:
        token = token.split(" ")[-1]
        data = jwt.decode(token, AUTH_SECRET_KEY, algorithms=["HS256"])
        wallet_id = data['wallet_id']
        wallet_object = Wallet.objects.get(id=wallet_id)
    except ExpiredSignatureError:
        raise exceptions.NotAuthenticated(
            detail="ٌtoken Expired", code=400)
    except ObjectDoesNotExist:
        raise exceptions.ValidationError(
            detail="ٌWallet object not exist", code=400)
    except:
        raise exceptions.ValidationError(
            detail="ٌcan\'n return wallet object", code=400)
    return wallet_object


# todo : verify token
def verify_token(token):
    try:
        jwt.decode(
            token, AUTH_SECRET_KEY, algorithms=["HS256"])
    except:
        return False

    return True


# todo : verify token for admin
def verify_token_for_admin(token):
    try:
        data = jwt.decode(
            token, AUTH_SECRET_KEY, algorithms=["HS256"])
    except:
        return False
    if data['role'] == 'admin':
        return True
    else:
        return False


def is_it_adviser(request):
    try:
        token = get_token(request)
    except:
        return False
    try:
        wallet = get_wallet(token)
    except:
        return False
    return Adviser.objects.filter(wallet=wallet).exists()


def is_it_teacher(request):
    try:
        token = get_token(request)
    except:
        return False
    try:
        wallet = get_wallet(token)
    except:
        return False
    return Teacher.objects.filter(wallet=wallet).exists()


def is_it_admin(request):
    try:
        token = get_token(request)
    except:
        return False
    return verify_token_for_admin(token)


# todo : Sent request and return response to client | requests data can set in data or serializer
def send_request_to_server(url, request_type, serializer=None, token=None, data_type=None, data={}):

    if request_type == "post":

        # * for post method without serializer
        if not serializer == None:
            data = dict(serializer.validated_data)

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }

        # ! for request with nested datetime's object can't use data and should use json
        if data_type == "json":
            response = requests.post(url, json=data, headers=headers)
        elif data_type == "files":
            response = requests.post(url, files=data, headers=headers)
        else:
            response = requests.post(url, data=data, headers=headers)

        return Response(response.json(), status=response.status_code)

    elif request_type == "delete":

        # * for post method without serializer
        if not serializer == None:
            data = dict(serializer.validated_data)

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }
        response = requests.delete(url, json=data, headers=headers)

        return Response(response.json(), status=response.status_code)

    elif request_type == "get":

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }
        response = requests.get(url, headers=headers)

        return Response(response.json(), status=response.status_code)


# todo : Grt token
def get_token(request):
    if 'Authorization' in request.headers:
        return request.headers['Authorization'].split(" ")[-1]
    else:
        raise exceptions.ValidationError(
            detail="ٌCan\'t found Token", code=404)


# todo : Create url ( check ROLE_ID )
def get_url_with_service_and_role(user_type, main_url):
    if user_type == "student":
        url = HOST + main_url + ROLE_ID_STUDENT + "/" + SERVICE_ID
    elif user_type == "teacher":
        url = HOST + main_url + ROLE_ID_TEACHER + "/" + SERVICE_ID
    elif user_type == "adviser":
        url = HOST + main_url + ROLE_ID_ADVISER + "/" + SERVICE_ID
    elif user_type == "admin":
        url = HOST + "/admin" + main_url
    else:
        raise exceptions.ValidationError(detail="Invalid type", code=400)
    return url


# todo DRY : Create url for login ( admin or user )
def get_url_admin_or_user(user_type, main_url):
    if user_type == "admin":
        url = HOST + "/admin" + main_url
    elif user_type == "user":
        url = HOST + main_url
    else:
        raise exceptions.ValidationError(detail="Invalid type", code=400)
    return url


def get_my_object(request, model):
    try:
        token = get_token(request)
        wallet = get_wallet(token)
        obj = model.objects.get(wallet=wallet)
        return obj
    except:
        raise ObjectDoesNotExist


def is_it_student(request):
    try:
        token = get_token(request)
    except:
        return False
    try:
        wallet = get_wallet(token)
    except:
        return False
    return Student.objects.filter(wallet=wallet).exists()


def create_obj_by_type(obj_type, new_wallet):
    if obj_type == "student":
        new_user = Student.objects.create(wallet=new_wallet)
    elif obj_type == "teacher":
        new_user = Teacher.objects.create(wallet=new_wallet)
    elif obj_type == "adviser":
        new_user = Adviser.objects.create(wallet=new_wallet)


def get_wallet_and_verify_token(request):
    token = get_token(request)
    if verify_token(token):
        wallet = get_wallet(token)
        return wallet
    else:
        return False


# todo : Create url ( for Address )
def get_url_for_address(user_type, main_url):
    if user_type == 'user':
        url = HOST + main_url
    elif user_type == "admin":
        url = HOST + "/admin" + main_url + "/my"
    else:
        raise exceptions.ValidationError(
            detail="Invalid user type", code=400)
    return url
