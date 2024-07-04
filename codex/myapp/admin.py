from django.contrib import admin
from myapp.models import userreg,profile,Repository,RepositoryData,Friends,Collaborators,History,Tasks

# Register your models here.
class Admin(admin.ModelAdmin):
     list_display=('id','fname','lname','uname','pwrd','email','phone','rights','at')
admin.site.register(userreg,Admin)

class Admin(admin.ModelAdmin):
     list_display=('id','user','designation','photo')
admin.site.register(profile,Admin)

class Admin(admin.ModelAdmin):
     list_display=('id','user','repoName','type','discription','created_at')
admin.site.register(Repository,Admin)

class Admin(admin.ModelAdmin):
     list_display=('id','repository','zipFile','uploaded_at')
admin.site.register(RepositoryData,Admin)

class Admin(admin.ModelAdmin):
     list_display=('id','user','friendEmail')
admin.site.register(Friends,Admin)

class Admin(admin.ModelAdmin):
     list_display=('id','user','collaborator','repository')
admin.site.register(Collaborators,Admin)

class Admin(admin.ModelAdmin):
     list_display=('id','event','occured_at')
admin.site.register(History,Admin)

class Admin(admin.ModelAdmin):
     list_display=('id','user','repository','task','collaborator')
admin.site.register(Tasks,Admin)