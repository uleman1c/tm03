from django.contrib.messages.storage import session
# from django.http import request
from django.shortcuts import redirect, render

from users1c.models import Users1c


def login(request):
    if 'userLogged' in request.session:
        return redirect('/') #w = 1 # return redirect(url('profile', username=session['userLogged']))
    elif request.method == 'POST' and user_allowed(request.POST['username'], request.POST['pwd']):
        request.session.permanent = request.POST.get('remember') == 'remember-me'
        request.session['userLogged'] = request.POST['username'].lower().strip()
        return redirect('/')

    return render(request, 'login.html', locals())


def user_allowed(username, pwd):
    return len(Users1c.objects.filter(name__exact=username.lower().strip(), pwd__exact=pwd).all()) == 1



def home(request):
    # return render(request, 'login.html', locals())
    return redirect('login')
