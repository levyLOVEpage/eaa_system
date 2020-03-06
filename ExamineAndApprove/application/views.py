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
    def get(self,request,applicant_id,format=None):
        queryset = ApplicantList.objects.filter(applicant_id=applicant_id)
        s = serializers.ApplySerializer(queryset,many=True)
        return Response({'status':
                             {'code':code.success_code[0],'msg':code.success_code[1]},
                         'data':s.data
                         })
    def post(self,request,format=None):
        s = serializers.ApplySerializer(data=request.data)
        if s.is_valid():
            s.save()
            return({'status':{'code':code.success_code[0],'msg':code.success_code[1]}})
        else:
            return({'status':{'code':code.error_2004[0],'msg':code.error_2004[1]}})




