from application.models import ApplicantList
from common.models import UserLogin
from application import serializers
from common.serializers import UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import jwt
import datetime
from common.extensions.auth import JwtAuthentication,create_token
from common.code import code
from common.extensions.pagination import LimitOffset
from django.db.models import Q




"""
pending页面
"""
class PendingList(APIView):
    authentication_classes = []
    def get(self,request,applicant_id,format=None):
        role = UserLogin.objects.filter(id=applicant_id).first()
        role_info = UserLoginSerializer(role)
        role_type = role_info.data['type']
        # 普通员工
        if role_type == 3:
            queryset = ApplicantList.objects.filter(Q(applicant_id=applicant_id)&Q(status="pendingSubmit"))
            total = queryset.count()
            page_obj = LimitOffset()
            page_list = page_obj.paginate_queryset(queryset=queryset, request=request, view=self)
            s = serializers.ApplySerializer(page_list, many=True)
            return Response({'status':
                                 {'code': code.success_code[0], 'msg': code.success_code[1]},
                             'data': s.data,
                             'total':total
                             })
        # 部门管理员
        elif role_type == 2:
            queryset = ApplicantList.objects.filter(Q(reviewer_id=applicant_id),Q(status="pendingSubmit")|Q(status="pendingApprove"))
            total = queryset.count()
            page_obj = LimitOffset()
            page_list = page_obj.paginate_queryset(queryset=queryset, request=request, view=self)
            s = serializers.ApplySerializer(page_list, many=True)
            return Response({'status':
                                 {'code': code.success_code[0], 'msg': code.success_code[1]},
                             'data': s.data,
                             'total': total
                             })
        elif role_type == 1:
            queryset = ApplicantList.objects.filter(Q(reviewer_id=applicant_id)&Q(status="pendingApprove"))
            total = queryset.count()
            page_obj = LimitOffset()
            page_list = page_obj.paginate_queryset(queryset=queryset, request=request, view=self)
            s = serializers.ApplySerializer(page_list, many=True)
            return Response({'status':
                                 {'code': code.success_code[0], 'msg': code.success_code[1]},
                             'data': s.data,
                             'total': total
                             })
        else:
            return Response({'status':
                                 {'code': code.error_2005[0], 'msg': code.error_2005[1]}
                             })
"""
个人apply页面
"""
class MyApply(APIView):
    authentication_classes = []
    def get(self,request,applicant_id,format=None):
        role = UserLogin.objects.filter(id=applicant_id).first()
        role_info = UserLoginSerializer(role)
        role_type = role_info.data['type']
        # 普通员工
        if role_type == 3:
            queryset = ApplicantList.objects.filter(Q(applicant_id=applicant_id),Q(status="pendingApprove")|Q(status="normalClose")|Q(status="timeoutClose"))
            total = queryset.count()
            page_obj = LimitOffset()
            page_list = page_obj.paginate_queryset(queryset=queryset, request=request, view=self)
            s = serializers.ApplySerializer(page_list, many=True)
            return Response({'status':
                                 {'code': code.success_code[0], 'msg': code.success_code[1]},
                             'data': s.data,
                             'total': total
                             })
        # 部门管理员
        elif role_type == 2:
            queryset = ApplicantList.objects.filter(Q(applicant_id=applicant_id),Q(status="pendingApprove")|Q(status="normalClose")|Q(status="timeoutClose"))
            total = queryset.count()
            page_obj = LimitOffset()
            page_list = page_obj.paginate_queryset(queryset=queryset, request=request, view=self)
            s = serializers.ApplySerializer(page_list, many=True)
            return Response({'status':
                                 {'code': code.success_code[0], 'msg': code.success_code[1]},
                             'data': s.data,
                             'total': total
                             })
        else:
            return Response({'status':
                                 {'code': code.error_2005[0], 'msg': code.error_2005[1]}
                             })
"""
所有申请页面
"""
class AllApply(APIView):
    authentication_classes = []
    def get(self,request,applicant_id,format=None):
        role = UserLogin.objects.filter(id=applicant_id).first()
        role_info = UserLoginSerializer(role)
        role_type = role_info.data['type']
        # 普通管理员
        if role_type == 2:
            queryset = ApplicantList.objects.filter(Q(reviewer_id=applicant_id),Q(status="pendingApprove")|Q(status="normalClose")|Q(status="timeoutClose"))
            total = queryset.count()
            page_obj = LimitOffset()
            page_list = page_obj.paginate_queryset(queryset=queryset, request=request, view=self)
            s = serializers.ApplySerializer(page_list, many=True)
            return Response({'status':
                                 {'code': code.success_code[0], 'msg': code.success_code[1]},
                             'data': s.data,
                             'total': total
                             })
        # 总管理员
        elif role_type == 1:
            queryset = ApplicantList.objects.filter(Q(status="pendingApprove")|Q(status="normalClose")|Q(status="timeoutClose"))
            total = queryset.count()
            page_obj = LimitOffset()
            page_list = page_obj.paginate_queryset(queryset=queryset, request=request, view=self)
            s = serializers.ApplySerializer(page_list, many=True)
            return Response({'status':
                                 {'code': code.success_code[0], 'msg': code.success_code[1]},
                             'data': s.data,
                             'total': total
                             })
        else:
            return Response({'status':
                                 {'code': code.error_2005[0], 'msg': code.error_2005[1]}
                             })
class Apply(APIView):
    authentication_classes = []
    def post(self,request,format=None):
        s = serializers.ApplySerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response({'status':{'code':code.success_code[0],'msg':code.success_code[1]}})
        else:
            return Response({'status':{'code':code.error_2004[0],'msg':code.error_2004[1]}})


