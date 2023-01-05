from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


CustomUser = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'accounts/signup.html', param)

def login_view(request):
    if request.method == 'POST':
        next = request.POST.get('next')
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = LoginForm()

    param = {
        'form': form,
    }

    return render(request, 'accounts/login.html', param)

class UserDeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = CustomUser.objects.get(username=self.request.user.username)
        user.is_active = False
        user.save()
        auth_logout(self.request)
        # ↓redirectに書き換える
        return redirect('login')
        # return render(self.request,'accounts/login.html')