from django.shortcuts import render,redirect 
from django.http import JsonResponse 
from myapp.models import userreg,profile,Repository,RepositoryData,Friends,Collaborators,History,Tasks
from django.contrib import messages
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.

def index(request):
    return render(request,'index.html')

#user account register
def register(request):
    if 'username' in request.session:
        if 'rights' in request.session:
         return redirect(user_Home)
        else:
            return redirect(adminHome)
    if request.method=="POST":
        firstname=request.POST.get('fname')
        lastname=request.POST.get('lname')
        usrname=request.POST.get('uname')
        paswrd=request.POST.get('pass')
        mail=request.POST.get('email')
        ph=request.POST.get('phone')
        encryptPassword=make_password(paswrd)
        r=userreg(fname=firstname,lname=lastname,uname=usrname,pwrd=encryptPassword,email=mail,phone=ph)
        r.save()
        event="New user registered-: "+usrname
        new_history=History(event=event)
        new_history.save()
        return redirect('/wlcm/')
    return render(request,'home.html')


#welcome page after user registering account
def welcomePage(request):
    return render(request,'userWelcome.html')
    

#user login with session
def user_login(request):
    if 'username' in request.session:
        if 'rights' in request.session:
         return redirect(user_Home)
        else:
            return redirect(adminHome)
    if request.method=="POST":
        Uname=request.POST.get('usrname')
        Pass=request.POST.get('pass')
        if userreg.objects.filter(uname=Uname).exists():
            userdata=userreg.objects.get(uname=Uname)
            retrived_pass=userdata.pwrd
            if userdata.rights=="user":
                if check_password(Pass,retrived_pass):
                    request.session['username']=Uname
                    request.session['rights']="user"
                    user=request.session.get('username')
                    event=user+" logged in"
                    new_history=History(event=event)
                    new_history.save()
                    return redirect(user_Home)
             
                else:
                    messages.error(request,'Invalid Password')
            else:
                if retrived_pass==Pass:
                    request.session['username']=Uname
                    return redirect(adminHome)
                else:
                    messages.error(request,'Invalid Password')
        else:
            messages.error(request,'Invalid Username')
    return render(request,'login.html')

#forgot password
def forgotPass(request):
    if request.method=="POST":
        username=request.POST.get('usrname')
        email=request.POST.get('email')
        password=request.POST.get('confirmpass')
        if userreg.objects.filter(uname=username).exists():
            userData=userreg.objects.get(uname=username)
            if email==userData.email:
                encryptPass=make_password(password)
                userData.pwrd=encryptPass
                userData.save()
                return redirect(register)
            else:
                messages.error(request,'Invalid Email')
        else:
            messages.error(request,'Invalid Username')
    return render(request,'forgotPassword.html')


#Admin Page
def adminHome(request):
     if 'username' in request.session:
        usrname=request.session.get('username')
        user_data=userreg.objects.get(uname=usrname)
        userdata={
                    'fname':user_data.fname,
                    'lname':user_data.lname,
                    'uname':user_data.uname,
                    'password':user_data.pwrd,
                    'email':user_data.email,
                    'phone':user_data.phone,
                    'createdAt':user_data.at,
                    
                }
        allUsers=userreg.objects.all()
        allProfile=profile.objects.all()
        user_and_profile=zip(allUsers,allProfile)
        if request.method=="POST":
            if 'deleteuser'in request.POST:
                Uname=request.POST.get('username')
                userreg.objects.filter(uname=Uname).delete()
        return render(request,'AdminHome.html',{'users_and_profile':user_and_profile,'userdata':userdata})
     return redirect(user_login)

#user session logout
def user_logout(request):
    if 'username' in request.session:
        user=request.session.get('username')
        event=user+" logged out"
        new_history=History(event=event)
        new_history.save()
        request.session.flush()
    return redirect('/h/')


#handels website history
def history(request):
    if 'username' in request.session:
        AllHistory=History.objects.all()
        return render(request,'history.html',{'WebsiteHistory':AllHistory})
    return redirect(user_login)
#user home Page
def user_Home(request):
    if 'username' in request.session:
        usrname=request.session.get('username')
        try:
            user_data=userreg.objects.get(uname=usrname)
            check_username=profile.objects.filter(user=user_data).exists()
            if check_username:
                Profile=profile.objects.get(user=user_data)
                userdata={
                    'fname':user_data.fname,
                    'lname':user_data.lname,
                    'uname':user_data.uname,
                    'password':user_data.pwrd,
                    'email':user_data.email,
                    'phone':user_data.phone,
                    'createdAt':user_data.at,
                    'profile_data':{
                        'designation':Profile.designation,
                        'pic':Profile.photo,
                    }
                }
                allUsers=userreg.objects.all()
                allProfile=profile.objects.all()
                user_and_profile=zip(allUsers,allProfile)
                if request.method=="POST":
                    if 'addfr'in request.POST:
                        email=request.POST.get('userEmail')
                        new_friend=Friends(user=user_data,friendEmail=email)
                        new_friend.save()
                    else:
                        email=request.POST.get('userEmail')
                        Friends.objects.filter(user=user_data,friendEmail=email).delete()
                return render(request,'user_Home.html',{'userdata':userdata,'users_and_profile':user_and_profile})
            else:
                return redirect(update_Profile)
        except profile.DoesNotExist:
            return redirect(update_Profile)
        except userreg.DoesNotExist:
            return redirect(user_login)
    return redirect(user_login)



#update Profile
def update_Profile(request):
    if 'username' in request.session:
       
        if request.method=='POST':
            username=request.session.get('username')
            user_data=userreg.objects.get(uname=username)
            UID=user_data.id
            try:
                usrprofile=profile.objects.get(user=user_data)
                usrprofile.designation=request.POST.get('designation')
                usrprofile.photo=request.FILES['pic']
                usrprofile.save()

                #adding to web history
                user=request.session.get('username')
                event=user+" updated their profile"
                new_history=History(event=event)
                new_history.save()

                return redirect(user_Home)
            except userreg.DoesNotExist:
                return redirect(user_login)
            except profile.DoesNotExist:
                dsg=request.POST.get('designation')
                pic=request.FILES['pic']
                p=profile(user=user_data,designation=dsg,photo=pic)
                p.save()

                 #adding to web history
                user=request.session.get('username')
                event=user+" updated their profile"
                new_history=History(event=event)
                new_history.save()

                return redirect(user_Home)
    return render(request,'profile.html')

#ajax live validation of username for user registration
def liveCheck(request):
    data={}
    mydata=request.GET.get('Data')
    if userreg.objects.filter(uname=mydata).exists():
        data['exists']=True
    else:
        data['exists']=False
    return JsonResponse(data)

#ajax live validation of phone number for user registration

def phoneCheck(request):
    data={}
    phonenum=request.POST.get('Phone')
    if userreg.objects.filter(phone=phonenum).exists():
        data['exists']=True
    else:
        data['exists']=False
    return JsonResponse(data)

#To render repository page 
def RepositoryHome(request):
    if 'username' in request.session:
        usrname=request.session.get('username')
        try:
            user_data=userreg.objects.get(uname=usrname)
            check_username=profile.objects.filter(user=user_data).exists()
            repo_count=Repository.objects.filter(user=user_data).count()
            repoDetails=Repository.objects.filter(user=user_data)
            if check_username:
                Profile=profile.objects.get(user=user_data)
                userdata={
                    'fname':user_data.fname,
                    'lname':user_data.lname,
                    'uname':user_data.uname,
                    'password':user_data.pwrd,
                    'email':user_data.email,
                    'phone':user_data.phone,
                    'createdAt':user_data.at,
                    'profile_data':{
                        'designation':Profile.designation,
                        'pic':Profile.photo,
                    },
                    'repoCount':{
                        'count':repo_count,
                    },
                    
                }
                if request.method=='POST':
                    if 'form1-submit' in request.POST:
                        reponame=request.POST.get('repo-name')
                        type=request.POST.get('repoType')
                        description=request.POST.get('description')
                        r=Repository(user= user_data,repoName=reponame,type=type,discription=description)
                        r.save()

                         #adding to web history
                        user=request.session.get('username')
                        event=user+" created a new repository- "+reponame
                        new_history=History(event=event)
                        new_history.save()

                    if 'form2-submit' in request.POST:
                        repoID=request.POST.get('RepoID')
                        zip=request.FILES['files']
                        repository=Repository.objects.get(id=repoID)
                        newRepoData=RepositoryData(repository=repository,zipFile=zip)
                        newRepoData.save()

                        #adding to web history
                        user=request.session.get('username')
                        RepoName=repository.repoName
                        event=user+" add a new project to "+RepoName
                        new_history=History(event=event)
                        new_history.save()

                return render(request,'repository.html',{'userdata':userdata,'repoDetails':repoDetails})
            else:
                return redirect(update_Profile)
        except profile.DoesNotExist:
            return redirect(update_Profile)
        except userreg.DoesNotExist:
            return redirect(user_login)
    return redirect(user_login)

#For dynamically checking for repository name availability using ajax
def checkReponame(request):
    response={}
    reponame=request.POST.get('Data')
    if Repository.objects.filter(repoName=reponame).exists():
        response['exists']=True
    else:
       response['exists']=False
    return JsonResponse(response)

#for opening repository
def openRepository(request):
    if 'username' in request.session:
        usrname=request.session.get('username')
        try:
            user_data=userreg.objects.get(uname=usrname)
            check_username=profile.objects.filter(user=user_data).exists()
           
            if check_username:
                Profile=profile.objects.get(user=user_data)
                userdata={
                    'fname':user_data.fname,
                    'lname':user_data.lname,
                    'uname':user_data.uname,
                    'password':user_data.pwrd,
                    'email':user_data.email,
                    'phone':user_data.phone,
                    'createdAt':user_data.at,
                    'profile_data':{
                        'designation':Profile.designation,
                        'pic':Profile.photo,
                    },
                    
                }
                param1 = request.GET.get('param1')
                R=Repository.objects.get(id=param1)
                F=Friends.objects.filter(user=user_data)
                task=Tasks.objects.filter(repository=R)
                friend_list=[]
                for friendsData in F:
                    fdata=userreg.objects.get(email=friendsData.friendEmail)
                    friend_list.append(fdata)
                if request.method=="POST":
                    if 'add-collab' in request.POST:
                        collab_username=request.POST.get('userName')
                        C=Collaborators(user=user_data,collaborator=collab_username,repository=R)
                        C.save()
                    if 'rm-collab' in request.POST:
                        collab_username=request.POST.get('userName')
                        Collaborators.objects.filter(repository=R,collaborator=collab_username).delete()
                    if 'addTask' in request.POST:
                        Cuname=request.POST.get('Cuname')
                        tasks=request.POST.get('task')
                        T=Tasks(user=user_data,repository=R,task=tasks,collaborator=Cuname)
                        T.save()
                if RepositoryData.objects.filter(repository=R).exists():
                    respose=True
                else:
                    respose=False
                return render(request,'openRepo.html',{'userdata':userdata,'Repo':R,'Friend':friend_list,'RepoDataPresent':respose,'Task':task})
            else:
                return redirect(update_Profile)
        except profile.DoesNotExist:
            return redirect(update_Profile)
        except userreg.DoesNotExist:
            return redirect(user_login)
    return redirect(user_login)

#For checking if a user is friend or not using ajax
def checkFriend(request):
  response={}
  Email=request.POST.get('Data')
  usrname=request.session.get('username')
  userInstance=userreg.objects.get(uname=usrname)
  if Friends.objects.filter(user=userInstance,friendEmail=Email).exists():
    response['exists']=True
  else:
    response['exists']=False
  return JsonResponse(response)

#For downloading file
def download_zip_file(request, repository_id):
    # Retrieve the repository data instance
    repository_data = get_object_or_404(RepositoryData, repository_id=repository_id)

    # Get the file path of the zip file
    file_path = os.path.join(settings.MEDIA_ROOT, str(repository_data.zipFile))

    # Open the zip file in binary mode for reading
    with open(file_path, 'rb') as f:
        # Prepare the HTTP response
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(file_path))
        return response

#check for collaborators
def checkCollab(request):
    response={}
    username=request.POST.get('Data')
    repoid=request.POST.get('Repo')
    repoInstance=Repository.objects.get(id=repoid)
    if Collaborators.objects.filter(repository=repoInstance,collaborator=username).exists():
        response['exists']=True
    else:
        response['exists']=False
    return JsonResponse(response)

#For shared page
def shared(request):
    if 'username' in request.session:
        usrname=request.session.get('username')
        try:
            user_data=userreg.objects.get(uname=usrname)
            check_username=profile.objects.filter(user=user_data).exists()
            if check_username:
                Profile=profile.objects.get(user=user_data)
                userdata={
                    'fname':user_data.fname,
                    'lname':user_data.lname,
                    'uname':user_data.uname,
                    'password':user_data.pwrd,
                    'email':user_data.email,
                    'phone':user_data.phone,
                    'createdAt':user_data.at,
                    'profile_data':{
                        'designation':Profile.designation,
                        'pic':Profile.photo,
                    }
                }
                if request.method=='POST':
                    if 'form2-submit' in request.POST:
                        repoID=request.POST.get('RepoID')
                        zip=request.FILES['files']
                        repository=Repository.objects.get(id=repoID)
                        if RepositoryData.objects.filter(repository=repository).exists():
                            RepositoryData.objects.filter(repository=repository).delete()
                            replaceRepoData=RepositoryData(repository=repository,zipFile=zip)
                            replaceRepoData.save()
                        else:
                            newRepoData=RepositoryData(repository=repository,zipFile=zip)
                            newRepoData.save()
                sharedProject_list=Collaborators.objects.filter(collaborator=usrname)
                return render(request,'shared.html',{'userdata':userdata,'shared':sharedProject_list})
            else:
                return redirect(update_Profile)
        except profile.DoesNotExist:
            return redirect(update_Profile)
        except userreg.DoesNotExist:
            return redirect(user_login)
    return redirect(user_login)
    

def openShared(request):
    if 'username' in request.session:
        usrname=request.session.get('username')
        try:
            user_data=userreg.objects.get(uname=usrname)
            check_username=profile.objects.filter(user=user_data).exists()
           
            if check_username:
                Profile=profile.objects.get(user=user_data)
                userdata={
                    'fname':user_data.fname,
                    'lname':user_data.lname,
                    'uname':user_data.uname,
                    'password':user_data.pwrd,
                    'email':user_data.email,
                    'phone':user_data.phone,
                    'createdAt':user_data.at,
                    'profile_data':{
                        'designation':Profile.designation,
                        'pic':Profile.photo,
                    },
                    
                }
                param1 = request.GET.get('param1')
                R=Repository.objects.get(id=param1)
                getCollab=Collaborators.objects.filter(repository=R)
                task=Tasks.objects.filter(repository=R,collaborator=user_data.uname)
                if request.method=="POST":
                    if 'complete' in request.POST:
                        taskId=request.POST.get('taskID')
                        status="Completed"
                        T=Tasks.objects.get(id=taskId)
                        T.status=status
                        T.save()
                if RepositoryData.objects.filter(repository=R).exists():
                    respose=True
                else:
                    respose=False
                return render(request,'openSharedRepo.html',{'userdata':userdata,'Repo':R,'Collabs':getCollab,'RepoDataPresent':respose,'Task':task})
            else:
                return redirect(update_Profile)
        except profile.DoesNotExist:
            return redirect(update_Profile)
        except userreg.DoesNotExist:
            return redirect(user_login)
    return redirect(user_login)
   
#for checking valid collaborators for adding task
def checkCollab(request):
    response={}
    repo=request.POST.get('Repo')
    Cuname=request.POST.get('Data')
    R=Repository.objects.get(id=repo)
    if Collaborators.objects.filter(repository=R,collaborator=Cuname).exists():
        response['exists']=True
    else:
        response['exists']=False
    return JsonResponse(response)

def checkEmail(request):
    data={}
    Email=request.POST.get('Email')
    if userreg.objects.filter(email=Email).exists():
        data['exists']=True
    else:
        data['exists']=False
    return JsonResponse(data)

def deleteAccount(request):
    if 'username' in request.session:
        usrname=request.session.get('username')
        try:
            user_data=userreg.objects.get(uname=usrname)
            check_username=profile.objects.filter(user=user_data).exists()
           
            if check_username:
                Profile=profile.objects.get(user=user_data)
                userdata={
                    'fname':user_data.fname,
                    'lname':user_data.lname,
                    'uname':user_data.uname,
                    'password':user_data.pwrd,
                    'email':user_data.email,
                    'phone':user_data.phone,
                    'createdAt':user_data.at,
                    'profile_data':{
                        'designation':Profile.designation,
                        'pic':Profile.photo,
                    },
                    
                }
               
                if request.method=="POST":
                    if 'form1-submit' in request.POST:
                        uname=request.POST.get('uname')
                        userreg.objects.filter(uname=uname).delete()
                        return redirect(user_logout)
                    if 'form2-submit' in request.POST:
                        reponame=request.POST.get('reponame')
                        Repository.objects.filter(repoName=reponame).delete()
                        return redirect(user_Home)
                return render(request,'deleteAccount.html',{'userdata':userdata,})
            else:
                return redirect(update_Profile)
        except profile.DoesNotExist:
            return redirect(update_Profile)
        except userreg.DoesNotExist:
            return redirect(user_login)
    return redirect(user_login)
    