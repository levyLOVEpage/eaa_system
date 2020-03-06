from rest_framework import serializers
from application import models

class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicantList
        fields = '__all__'