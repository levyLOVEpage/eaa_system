# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models




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
