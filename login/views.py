from django.contrib.messages.storage import session
# from django.http import request
from django.shortcuts import redirect, render

from users1c.models import Users1c


def login(request):
    
    if request.method == 'GET':

        ret = request.GET.get('ret')
        if not ret:
            ret = ''

        if 'userLogged' in request.session:
            return redirect('/') #w = 1 # return redirect(url('profile', username=session['userLogged']))
    
        return render(request, 'login.html', locals())

    elif request.method == 'POST':
        
        if user_allowed(request.POST['username'], request.POST['pwd']):
            request.session.permanent = request.POST.get('remember') == 'remember-me'
            request.session['userLogged'] = request.POST['username'].lower().strip()

            return redirect('..' + request.POST['ret'])

        else:
                
            ret = request.POST.get('ret')
            if not ret:
                ret = ''

            return render(request, 'login.html', locals())



def user_allowed(username, pwd):
    return len(Users1c.objects.filter(name__exact=username.lower().strip(), pwd__exact=pwd).all()) == 1



def home(request):
    # return render(request, 'login.html', locals())
    return redirect('login')
