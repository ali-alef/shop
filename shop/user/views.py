from django.shortcuts import render, redirect
from .forms import userRegisterFrom
from django.contrib.auth.views import LogoutView
from store.models import Customer
from store.functions import getCartSpec
from django.contrib.auth import authenticate, login
from store.functions import mergeItems


def registerView(request):
    if request.method == 'POST':
        form = userRegisterFrom(request.POST)
        if form.is_valid():
            user = form.save()
            email = request.POST.get('email')
            name = request.POST.get('username')

            Customer.objects.create(user=user, email=email, name=name)

            return redirect('login')
    else:
        form = userRegisterFrom()

    _, _, cartItems = getCartSpec(request)

    return render(request, 'user/register.html', {'form': form, 'cartItems': cartItems})


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            mergeItems(request)
            return redirect('store')
        else:
            return redirect('login_user')

    else:
        _, _, cartItems = getCartSpec(request)
        form = userRegisterFrom()

        return render(request, 'user/login.html', context={'form': form, 'cartItems': cartItems})


class LogoutViewCustom(LogoutView):
    template_name = 'user/logout.html'

    def get_context_data(self, **kwargs):
        context = super(LogoutViewCustom, self).get_context_data(**kwargs)
        _, _, context['cartItems'] = getCartSpec(self.request)

        return context
