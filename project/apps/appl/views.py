from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
from django.contrib import messages
from .models import User, Challenge, Message
from django.core.files.storage import FileSystemStorage
import bcrypt


def upload(request, id): 
    if request.method == 'POST' and request.POST['content'] != "":
        newmessage = Message.objects.create(
        content = request.POST['content'],
        sender = User.objects.get(id=request.session['id']),
        competition = Challenge.objects.get(id=id))
    return redirect(f'/challenge/{id}') 

def display(request): 
  
    if request.method == 'GET': 
  
 
        messages = Message.objects.all()  
        return render(request, 'appl/display.html',{'hotel_images' : messages})
  
def success(request): 
    return HttpResponse('successfuly uploaded')

def index(request):
    return render(request, 'appl/index.html')

def login(request):
    return render(request, 'appl/login.html')

def logprocess(request):
    errors = User.objects.log_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else: 
        logger = User.objects.filter(email= request.POST['login_email']).values()
        print(logger[0])
        request.session['username'] = logger[0]['username']
        request.session['id'] = logger[0]['id']
        return redirect('/dashboard')

def logout(request):
    request.session['username'] = None
    request.session['id'] = None
    return redirect('/')



def registration(request):
    return render(request, 'appl/registration.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/registration')
    else:
        new_user = User.objects.create( username=request.POST['username'], email = request.POST['email'], password = hash, bench = request.POST['bench'], squat = request.POST['squat'], deadlift = request.POST['deadlift'])
        print(new_user)
        user = User.objects.get(email = request.POST['email'])
        request.session['username'] = request.POST['username']
        request.session['id'] = user.id
        return redirect('/dashboard')

def dashboard(request):
    if request.session['id'] == None:
        return redirect('/')
    else:
        

        availables = []
        challenges = Challenge.objects.all()
        print(challenges)
        for challenge in challenges:
            people = challenge.joiners.all()
            for person in people:
                if person.id == request.session['id']:
                    print(challenge.name + "challenge is ok")
                    availables.append(Challenge.objects.get(id=challenge.id))
                    print(availables)
        context = {"challenges" : availables}
        print(context)
        return render(request, 'appl/dashboard.html', context)

def challenge(request, id):
    Messages = Message.objects.all()  
    Me = User.objects.get(id = request.session['id'])
    this_challenge = Challenge.objects.get(id=id)
    messages = Message.objects.filter(competition_id = id)
    context = {"information" : Challenge.objects.get(id=id),
    'benchers' : this_challenge.joiners.all().order_by('-bench'),
    'squatters' : this_challenge.joiners.all().order_by('-squat'),
    'lifters' : this_challenge.joiners.all().order_by('-deadlift'),
    'messages' : messages,
    'me' : Me
    }
    
    print(messages)


    return render(request, 'appl/challenge.html', context) 

def create(request):
    context = {"users" : User.objects.exclude(id = request.session['id'])}
    return render(request, 'appl/create.html', context)

def createprocess(request):
    errors = Challenge.objects.challenge_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/create')
    else:
        user_id = request.session['id']
        new_challenge = Challenge.objects.create(
            name=request.POST['name'], 
            goal = request.POST['goal'], 
            stakes = request.POST['stakes'], 
            end = request.POST['edate'],
            creator = User.objects.get(id=request.session['id']))
            
        invites=request.POST.getlist('invites')
        for invite in invites:
            person = User.objects.get(id=int(invite))
            print(person)
            new_challenge.joiners.add(person)
        maker = User.objects.get(id=request.session['id'])
 
        new_challenge.joiners.add(maker)

        print(request.POST.getlist('invites'))
        return redirect('/dashboard')

def remove(request, id):
    d = Challenge.objects.get(id=id)
    d.delete()
    return redirect('/dashboard')


def update(request, id, user_id):
    update_user = User.objects.get(id = user_id)
    print(update_user)
    if request.POST['bench'] != 0 and request.POST['bench'] != None:
        update_user.bench = request.POST['bench'] 
        update_user.save()
    if request.POST['squat'] != 0 and request.POST['squat'] != None:
        update_user.squat = request.POST['squat'] 
        update_user.save()
    if request.POST['deadlift'] != 0 and request.POST['deadlift'] != None:
        update_user.deadlift = request.POST['deadlift'] 
        update_user.save()

    return redirect(f'/challenge/{id}')

