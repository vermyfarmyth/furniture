from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from orders.models import Order
from reviews.models import Review

from .forms import ProfileForm, RegisterForm, UserForm
from .models import Profile


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('core:home')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:login')



def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        messages.success(request, 'Регистрация успешна.')
        login(request, user)
        return redirect('core:home')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    user_form = UserForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile_obj)

    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, 'Профиль обновлен.')
        return redirect('accounts:profile')

    return render(
        request,
        'accounts/profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'my_orders': Order.objects.filter(user=request.user)[:5],
            'my_reviews': Review.objects.filter(user=request.user)[:5],
        },
    )
