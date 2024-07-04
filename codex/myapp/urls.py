from django.urls import path
from . import views
urlpatterns=[
    path('',views.index),
    path('h/',views.register),
    path('in/',views.index),
    path('wlcm/',views.welcomePage),
    path('usrlogin/',views.user_login,name="log"),
    path('usrlogout/',views.user_logout),
    path('forgotPassword/',views.forgotPass),
    path('userHome/',views.user_Home),
    path('adminHome/',views.adminHome),
    path('history/',views.history),
    path('updateProfile/',views.update_Profile),
    path('checkdata/',views.liveCheck),
    path('checkPhone/',views.phoneCheck),
    path('repo/',views.RepositoryHome),
    path('checkReponame/',views.checkReponame),
    path('openRepo/',views.openRepository),
    path('checkFr/',views.checkFriend),
     path('download-zip/<int:repository_id>/', views.download_zip_file, name='download_zip_file'),
    path('checkCollab/',views.checkCollab),
    path('sharedwithme/',views.shared),
    path('openSharedRepo/',views.openShared),
    path('checkCollab/',views.checkCollab),
    path('checkEmail/',views.checkEmail),
    path('deleteAccount/',views.deleteAccount)
   
]