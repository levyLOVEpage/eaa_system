from application.models import ApplicantList
from application import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import jwt
import datetime
from common.extensions.auth import JwtAuthentication,create_token
from common.code import code
from common.extensions.pagination import LimitOffset
class ApplyList(APIView):
    authentication_classes = []
    def get(self,request,applicant_id,format=None):
        queryset = ApplicantList.objects.filter(applicant_id=applicant_id)
        s = serializers.ApplySerializer(queryset,many=True)

        page_obj = LimitOffset()

        apply_list ={'status':
                             {'code':code.success_code[0],'msg':code.success_code[1]},
                         'data':s.data
                         }
        page_list = page_obj.paginate_queryset(queryset=queryset,request=request, view=self)
        s = serializers.ApplySerializer(page_list,many=True)
        return Response(s.data)
class Apply(APIView):
    authentication_classes = []
    def post(self,request,format=None):
        s = serializers.ApplySerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response({'status':{'code':code.success_code[0],'msg':code.success_code[1]}})
        else:
            return Response({'status':{'code':code.error_2004[0],'msg':code.error_2004[1]}})


