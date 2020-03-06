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
    applicant_name = models.CharField(max_length=32, blank=True, null=True)
    applicant_id = models.CharField(max_length=32, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    usage = models.CharField(max_length=32, blank=True, null=True)
    apply_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    reviewer_name = models.CharField(max_length=32, blank=True, null=True)
    reviewer_id = models.CharField(max_length=32, blank=True, null=True)
    applicant_department = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'applicant_list'
