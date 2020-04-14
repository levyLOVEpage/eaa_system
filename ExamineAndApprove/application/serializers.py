from rest_framework import serializers
from application import models

class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicantList
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Approval
        fields = '__all__'

class ApplicantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicantList
        fields = '__all__'