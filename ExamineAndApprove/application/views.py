from application.models import ApplicantList
from application import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import jwt
import datetime
from common.extensions.auth import JwtAuthentication,create_token
from common.code import code
class Apply(APIView):
    authentication_classes = []
    def get(self,applicant_id,format=None):
        queryset = ApplicantList.objects.all(applicant_id=applicant_id)
        s = serializers.ApplySerializer(queryset)
        return Response({'status':
                             {'code':code.success_code[0],'msg':code.success_code[1]},
                         'data':s.data
                         })




