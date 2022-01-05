import jwt
import datetime

from decouple import config


def make_token(obj):
    return jwt.encode(
        {
            "id": f"{obj.wallet.pk}",
            "role": "user",
            "service": config("SERVICE_ID"),
            "packet_id": "dded429f-852b-47ca-aafd-c0285350a5a7",
            "username": "whatever",
            "wallet_id": f"{obj.wallet.pk}",
            "iat": datetime.datetime.now(),
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        },
        config("AUTH_SECRET_KEY"),
        algorithm="HS256",
    )


def make_admin_token():
    return jwt.encode(
        {
            "id": "6a08a939-1b3d-42b9-9fc3-7447e0fbd3d6",
            "role": "admin",
            "service": config("SERVICE_ID"),
            "packet_id": "dded429f-852b-47ca-aafd-c0285350a5a7",
            "username": "learning_admin",
            "wallet_id": "6e4818fb-4000-47be-8d05-1510e1efdff2",
            "iat": datetime.datetime.now(),
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        },
        config("AUTH_SECRET_KEY"),
        algorithm="HS256",
    )
