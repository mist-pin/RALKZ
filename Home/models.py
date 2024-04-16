from django.db import models
from Auth.models import RalkzUser



class Project(models.Model):
    id = models.SmallAutoField(primary_key=True)
    owner = models.ForeignKey(RalkzUser, on_delete=models.PROTECT)
    project_name = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="order placed")
    project_description = models.TextField()
    ordered_date = models.DateField(auto_now_add=True)
    project_init_date = models.DateField(null=True, blank=True)
    project_finish_date = models.DateField(null=True, blank=True)
    user_agreement = models.FileField(null=True, blank=True)
    git_link = models.TextField(null=True, blank=True)
    project_team = models.CharField(max_length=20, null=True, blank=True)
    estimated_cost = models.IntegerField(null=True, blank=True)
    is_update = models.BooleanField(default=False)
    root_project = models.ForeignKey('self',on_delete=models.PROTECT, null=True, blank=True)  # the base project id of the update is linked here.


class Aspirants(models.Model):
    id = models.SmallAutoField(primary_key=True)
    user = models.ForeignKey(RalkzUser, on_delete=models.PROTECT)
    application_status = models.CharField(max_length=20, default='submitted')
    submission_date = models.DateTimeField(auto_now=True)
    application_final_verified_date = models.DateField(null=True)  # hired or rejected date
    resume = models.FileField(upload_to="resume/%Y/", max_length=200)
    identity_proof = models.FileField(upload_to="identity/%Y/", max_length=200)
    study_certificate = models.FileField(upload_to="study_certificate/%Y/", max_length=200)
    experience_proof = models.FileField(upload_to="experience_proof/%Y/", max_length=200, null=True)

class Income(models.Model):
    id = models.SmallAutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20)  # one of advance, leftover, full
    amount = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
