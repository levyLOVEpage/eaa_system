from django.conf import settings
from rest_framework.authentication import BaseAuthentication
import jwt
from jwt import exceptions
from rest_framework.exceptions import AuthenticationFailed
import datetime
from rest_framework.response import Response
class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token =request.META.get("HTTP_AUTHORIZATION")
        salt = settings.SECRET_KEY
        payload = None
        msg = None
        try:
            payload = jwt.decode(token,salt,True)
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code':1000,'msg':"token已失效"})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code':1001,'msg':"token认证失败"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 1002, 'msg': "非法的token"})
        return (payload,token)
def create_token(payload,timeout=30):
    salt = settings.SECRET_KEY
    headers = {
        "type":'jwt',
        'alg':'HS256'
    }
    payload['exp']=datetime.datetime.utcnow()+datetime.timedelta(days=timeout)
    token = jwt.encode(payload=payload,key=salt,algorithm='HS256',headers=headers).decode('utf-8')
    return token