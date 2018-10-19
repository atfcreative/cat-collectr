#-----main_app/views.py --------#

#import redirect-
from django.shortcuts import render, redirect
from .models import Cat
from .forms import CatForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# from django.http import HttpResponse

#index cat page
def index(request):
    cats = Cat.objects.all()
    form = CatForm()
    return render(request, 'index.html', { 'cats':cats, 'form':form })
    # return HttpResponse('<h1>Hello World! U+1F44B</h1>')
    # return render(request, 'index.html')

#show one cat
def show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'show.html', { 'cat': cat })

#create(post) one cat
def post_cat(request):
    form = CatForm(request.POST)
    if form.is_valid():
        cat = form.save(commit = False)
        cat.user = request.user
        cat.save()
    return redirect('/')

def profile(request, username):
    user = User.objects.get(username = username)
    cats = Cat.objects.filter(user = user)
    return render(request, 'profile.html', { 'username': username, 'cats': cats })

def login_view(request):
    if request.method == 'POST':
        #if its a post, then auth. it (user sent pw & username)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user. is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def like_cat(request):
    cat_id = request.GET.get('cat_id', None)

    likes = 0
    if(cat_id):
        cat = Cat.objects.get(id = int(cat_id))
        if cat is not None:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# cats = [
#     Cat('Mr. Bigglesworth', 'Hairless', 'Dr. Evils Cat', 1),
#     Cat('Stimpy', 'Cartoon', 'From Ren & Stimpy', 7),
#     Cat('Tunces', 'Driving', 'The Driving Cat', 69)
# ]

# def index(request):
#     return render(request, 'index.html', {'cats': cats})
