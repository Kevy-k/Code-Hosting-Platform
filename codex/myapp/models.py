from django.db import models

# Create your models here.
class userreg(models.Model):
    fname=models.CharField(max_length=25)
    lname=models.CharField(max_length=25)
    uname=models.CharField(max_length=25,unique=True)
    pwrd=models.CharField(max_length=20)
    email=models.EmailField(max_length=254)
    phone=models.CharField(max_length=10)
    rights=models.CharField(max_length=10,default="user")
    at=models.DateTimeField(auto_now_add=True)
    

class profile(models.Model):
    user=models.OneToOneField(userreg, on_delete=models.CASCADE)
    designation=models.CharField(max_length=40)
    photo=models.ImageField(upload_to='images/')



class Repository(models.Model):
    user=models.ForeignKey(userreg, on_delete=models.CASCADE)
    repoName=models.CharField(max_length=100,unique=True)
    type=models.CharField(max_length=15)
    discription=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        # Remove unique constraint on user_id
        unique_together = ('user', 'repoName',)

class RepositoryData(models.Model):
    repository=models.ForeignKey(Repository, on_delete=models.CASCADE)
    zipFile=models.FileField(upload_to='uploads/')
    uploaded_at=models.DateTimeField(auto_now_add=True)

class Friends(models.Model):
    user=models.ForeignKey(userreg, on_delete=models.CASCADE)
    friendEmail=models.CharField(max_length=255)

class Collaborators(models.Model):
    user=models.ForeignKey(userreg,on_delete=models.CASCADE)
    collaborator=models.CharField(max_length=25)
    repository=models.ForeignKey(Repository,on_delete=models.CASCADE)

class History(models.Model):
    event=models.CharField(max_length=35)
    occured_at=models.DateTimeField(auto_now_add=True)

class Tasks(models.Model):
    user=models.ForeignKey(userreg,on_delete=models.CASCADE)
    repository=models.ForeignKey(Repository,on_delete=models.CASCADE)
    task=models.CharField(max_length=255)
    collaborator=models.CharField(max_length=25)
    status=models.CharField(max_length=20,default="Active")