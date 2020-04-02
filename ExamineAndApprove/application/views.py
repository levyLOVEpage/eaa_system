from application.models import ApplicantList,Device,Department,Region
from common.models import UserLogin
from application import serializers
from common.serializers import UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import jwt
import datetime
from common.extensions.auth import JwtAuthentication,create_token,decode_token
from common.code import code
from common.extensions.pagination import LimitOffset
from django.db.models import Q
from rest_framework import request

class PendingList(APIView):
    """
    pending页面
    """
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

class MyApply(APIView):
    """
    个人apply页面
    """
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

class AllApply(APIView):
    """
    所有申请页面
    """
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
    def put(self,request,*args,**kwargs):
        if len(request.data['reviewer_id'])==2:
            obj = ApplicantList.objects.get(process_id=request.data['process_id'])
            obj.status='pendingApprove'
            obj.reviewer_id = request.data['reviewer_id'][0]
            obj.manager_id = request.data['reviewer_id'][1]
            obj.apply_time = request.data['apply_time']
            obj.save()
        elif len(request.data['reviewer_id'])==1:
            obj = ApplicantList.objects.get(process_id=request.data['process_id'])
            obj.status = 'pendingApprove'
            obj.reviewer_id = request.data['reviewer_id'][0]
            obj.apply_time = request.data['apply_time']
            obj.save()
        return Response({'status':{'code':code.success_code[0],'msg':code.success_code[1]}})
    def post(self,request,format=None):
        if request.data['coordination']==True:
            request.data['coordination']=1
        else:
            request.data['coordination']=0
        obj = ApplicantList(
            type=request.data['type'],
            applicant_id=request.data['applicant_id'],
            applicant_name=request.data['applicant_name'],
            apply_time=request.data['apply_time'],
            usage=request.data['usage'],
            telephone=request.data['telephone'],
            coordination=request.data['coordination'],
            auth_list=request.data['AuthList'],
            status='pendingSubmit'
        )
        obj.save()
        return Response({'process_id':obj.process_id,'status':{'code':code.success_code[0],'msg':code.success_code[1]}})


class ResourceList(APIView):
    authentication_classes = []
    def get(self,request,department_id,*args,**kwargs):

        tree_data = [
        {
            'key':'10000000',
            'title':'中国',
            'children':[{
                'key':'33000000',
                'title':'浙江省',
                'children':[{
                    'key':'33000001',
                    'title':'杭州市',
                    'children':[
                        {
                            'key':'35002',
                            'title':'AI探头2'
                        },
                    ]
                },
                    {
                        'key': '33000002',
                        'title': '温州市',
                        'children': [
                            {
                                'key': '35003',
                                'title': 'AI探头3'
                            },
                        ]
                    },
                    {
                        'key': '33000003',
                        'title': '宁波市',
                        'children': [
                            {
                                'key': '35004',
                                'title': 'AI探头4'
                            },
                        ]
                    },
                {
                    'key':'35001',
                    'title':'AI探头1',
                }]
            },{
                'key':'34000000',
                'title':'江苏省',
                'children':[{
                    'key':'34000001',
                    'title':'南京市',
                    'children':[
                        {
                            'key':'35006',
                            'title':'AI探头6'
                        }
                    ]
                },
                {
                    'key':'35005',
                    'title':'AI探头5',
                }]
            },{
                'key':'35007',
                'title':'AI探头7'
            }]
        }
        ]

        tree_data2 = [
        {
            'key':'10000000',
            'title':'中国',
            'children':[{
                'key':'35000000',
                'title':'广东省',
                'children':[{
                    'key':'35000001',
                    'title':'广州市',
                    'children':[
                        {
                            'key':'36009',
                            'title':'监控摄像头2'
                        },
                    ]
                },
                    {
                        'key': '35000002',
                        'title': '深圳市',
                        'children': [
                            {
                                'key': '36010',
                                'title': '监控摄像头3'
                            },
                        ]
                    },
                    {
                        'key': '35000003',
                        'title': '中山市',
                        'children': [
                            {
                                'key': '36011',
                                'title': '监控摄像头4'
                            },
                        ]
                    },
                {
                    'key':'36008',
                    'title':'监控摄像头1',
                }]
            },{
                'key':'36000000',
                'title':'四川省',
                'children':[{
                    'key':'36000001',
                    'title':'成都市',
                    'children':[
                        {
                            'key':'36013',
                            'title':'监控摄像头6'
                        }
                    ]
                },
                {
                    'key':'36012',
                    'title':'监控摄像头5',
                }]
            },{
                'key':'36014',
                'title':'监控摄像头7'
            }]
        }
        ]
        if department_id=='12':
            return Response(tree_data)
        elif department_id=='14':
            return Response(tree_data2)



class ResoucreQueryName(APIView):
    authentication_classes = []
    def post(self,request,*args,**kwargs):
        query = request.data['selected_resource']
        query_list = list(query)
        result_list = []
        for i in range(len(query_list)):
            if len(query_list[i])==5:
                r = Device.objects.get(device_id=query_list[i])
                result_list.append({'key':r.device_id,'name':r.device_name,'type':'device'})
            elif len(query_list[i])==8:
                r = Region.objects.get(region_id=query_list[i])
                result_list.append({'key': r.region_id, 'name': r.region_name, 'type': 'region'})
        return Response({'data':result_list})

class ReviewerQuery(APIView):
    authentication_classes = []
    def post(self,request,*args,**kwargs):
        department_id = request.data['department_id']
        query = Department.objects.filter(department_id=department_id)
        s = serializers.DepartmentSerializer(query,many=True)
        # query_list = list(query)
        # result_list = []
        # for i in range(len(query_list)):
        #     if len(query_list[i])==5:
        #         r = Device.objects.get(device_id=query_list[i])
        #         reviewer1 = Department.objects.filter(department_id=r.origin_department_id)
        #         reviewer1 = serializers.DepartmentSerializer(reviewer1,many=True)
        #         result_list.append({query_list[i]:reviewer1.data})
        #     elif len(query_list[i])==8:
        #         r = Device.objects.get(region_id=query_list[i])
        #         reviewer2 = Department.objects.filter(department_id=r.origin_department_id)
        #         reviewer2 = serializers.DepartmentSerializer(reviewer2,many=True)
        #         result_list.append({query_list[i]:reviewer2.data})
        return Response({'department_manager':s.data,'global_manager':{
                    "id": 4,
                    "department_id": "13",
                    "department_name": "总裁部",
                    "manager_id": "2",
                    "manager_name": "总裁办"
                }})
class PendingSubmitDetail(APIView):
    authentication_classes = []
    def get(self,request,process_id,*args,**kwargs):
        detail = ApplicantList.objects.get(process_id=process_id)
        return Response({
            'type':detail.type,
            'usage':detail.usage,
            'Telephone':detail.telephone,
            'coordination':detail.coordination,
            # 'AuthList':[{
            #     'OriginProcessId':detail.origin_process_id,
            #     'Department':detail.resource_department,
            #     'Period':{
            #         'startTime':detail.start_time,
            #         'endTime':detail.end_time
            #     },
            #     'Authority':detail.authority,
            #     'AttrList':detail.attr_list,
            #     'DeviceList':detail.resource_list
            # }]
            "AuthList":detail.auth_list
        })


