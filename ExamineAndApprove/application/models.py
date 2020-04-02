# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApplicantList(models.Model):
    process_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    coordination = models.IntegerField(blank=True, null=True)
    origin_process_id = models.IntegerField(blank=True, null=True)
    authority = models.CharField(max_length=255, blank=True, null=True)
    applicant_name = models.CharField(max_length=32, blank=True, null=True)
    applicant_id = models.CharField(max_length=32, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    usage = models.CharField(max_length=32, blank=True, null=True)
    apply_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    reviewer_name = models.CharField(max_length=32, blank=True, null=True)
    manager_id = models.IntegerField(blank=True, null=True)
    reviewer_id = models.CharField(max_length=1000, blank=True, null=True)
    applicant_department = models.CharField(max_length=255, blank=True, null=True)
    resource_department = models.CharField(max_length=255, blank=True, null=True)
    resource_list = models.CharField(max_length=255, blank=True, null=True)
    attr_list = models.CharField(max_length=255, blank=True, null=True)
    auth_list = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'applicant_list'


class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    department_id = models.CharField(max_length=255, blank=True, null=True)
    department_name = models.CharField(max_length=255, blank=True, null=True)
    manager_id = models.CharField(max_length=255, blank=True, null=True)
    manager_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class Device(models.Model):
    device_id = models.CharField(primary_key=True, max_length=255)
    resource_id = models.CharField(max_length=255, blank=True, null=True)
    device_name = models.CharField(max_length=255, blank=True, null=True)
    origin_department_id = models.CharField(max_length=255, blank=True, null=True)
    region_id = models.CharField(db_column='Region_id', max_length=64, blank=True, null=True)  # Field name made lowercase.
    region_name = models.CharField(db_column='Region_name', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'device'


class Region(models.Model):
    region_id = models.CharField(primary_key=True, max_length=255)
    region_name = models.CharField(max_length=255, blank=True, null=True)
    region_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region'


class UserLogin(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    account = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=16, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    department_name = models.CharField(max_length=16, blank=True, null=True)
    department_id = models.CharField(max_length=16, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_login'
