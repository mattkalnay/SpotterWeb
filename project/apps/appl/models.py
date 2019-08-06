from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class LoginManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if User.objects.filter(email = postData['email']):
            errors['email_exists'] = "An account associated with that email address already exists."
        if len(postData['username']) < 4:
            errors["username"] = "Username should be at least 4 characters"
        if EMAIL_REGEX.match(postData['email']) == None:
            errors['email_format'] = "Email must be in valid email format."
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least  8 characters"
        if postData['password'] != postData['password_con']:
            errors['password_con'] = "Password and Password Confirmation Do Not Match"
        print(errors)
        return errors

    def log_validator(self, postData):
        errors = {}
        user =  User.objects.filter(email = postData['login_email'])
        if not user:
            errors['email'] = "Email does not match our records"
        if user and not bcrypt.checkpw(postData['login_pass'].encode('utf8'), user[0].password.encode('utf8')):
            errors['password'] = "Invalid password."
        return errors

class ChallengeManager(models.Manager):
    def challenge_validator(self, postData):
        errors = {}
        if len(postData['name']) < 4:
            errors['name'] = "Name must be included"
        if len(postData['goal']) < 4:
            errors['goal'] = "Goal must be included"
        return errors
        




class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    bench = models.IntegerField()
    squat = models.IntegerField()
    deadlift = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

    def __repr__(self):
        return f"<User object: {self.username} {self.id}>"



class Challenge(models.Model):
    name = models.CharField(max_length=45)
    goal = models.CharField(max_length=100)
    stakes = models.CharField(max_length=100)
    start = models.DateTimeField(auto_now_add=True)
    end =  models.DateTimeField(default=None, blank=True, null=True)
    creator = models.ForeignKey(User, related_name='host_challenges')
    joiners = models.ManyToManyField(User, related_name='join_challenges')
    start_weight=models.IntegerField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChallengeManager()

    def __repr__(self):
        return f"<Challenge object: {self.name} {self.id}>"

class Message(models.Model): 
    content = models.TextField(default=None, blank=True, null=True) 
    sender = models.ForeignKey(User, related_name='messaging')
    competition = models.ForeignKey(Challenge, related_name='receiver')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)