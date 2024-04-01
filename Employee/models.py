from django.db import models
from Auth.models import RalkzUser
from Home.models import Project

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, primary_key=True)
    user_name = models.ForeignKey(RalkzUser, on_delete=models.PROTECT)
    join_date = models.DateField(auto_now_add=True)
    resign_date = models.DateField(null=True, blank=True)

class ScorePattern(models.Model):
    id = models.SmallAutoField(primary_key=True)


class ScoreAchieved(models.Model):
    id = models.SmallAutoField(primary_key=True)


class Score(models.Model):
    id = models.SmallAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    score_allotted = models.IntegerField()
    score_pattern = models.ForeignKey(ScorePattern, on_delete=models.PROTECT)
    score_achieved = models.ForeignKey(ScoreAchieved, on_delete=models.PROTECT)


class Salary(models.Model):
    id = models.SmallAutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    payment_proof = models.TextField()


class EmployeePosition(models.Model):
    id = models.SmallAutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    position = models.CharField(max_length=20)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)


class Team(models.Model):
    id = models.SmallAutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    team_name = models.CharField(max_length=20)