from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import datetime

from .models import UserProfile
from . import forms


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    user_profile = UserProfile.objects.first()
                    return render(request,
                                  'accounts/profile/display_profile.html',
                                  {'user_profile': user_profile})
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            if (UserProfile.objects.count() == 0):
                user_profile = UserProfile.objects.create(
                    first_name="Default",
                    last_name="Person",
                    dob = datetime.datetime.now(),
                    email = "default@gmail.com",
                    confirm_email = "default@gmail.com",
                    short_bio = "fill me in now, please",
                    avatar = ""
                )
            else:
                user_profile = UserProfile.objects.first()
            return render(request, 'accounts/profile/edit_profile.html',
                          {'user_profile': user_profile})
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_profile(request):
    user_profile = get_object_or_404(UserProfile)
    return render(request, 'accounts/profile/display_profile.html',
                  {'user_profile': user_profile})


@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile)
    form = forms.UserProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = forms.UserProfileForm(instance=user_profile, data=request.POST,
                                     files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Updated {}".format(
                                 form.cleaned_data['first_name'] + " " +
                                 form.cleaned_data['last_name']
                             ))
            return render(request, 'accounts/profile/edit_profile.html',
                          {'form': form, 'user_profile': user_profile})
    return render(request, 'accounts/profile/edit_profile.html',
                  {'form': form, 'user_profile': user_profile})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = forms.ValidatingPasswordChangeForm(request.user, request.POST)
        user_profile = get_object_or_404(UserProfile)
        #import pdb
        #pdb.set_trace()
        if user_profile.first_name in request.POST['new_password1']:
            messages.error(request, 'The new password may not contain the '
                                    'first name')
        elif user_profile.last_name in request.POST['new_password1']:
            messages.error(request, 'The new password may not contain the '
                                    'last name')
        elif request.user.username in request.POST['new_password1']:
            messages.error(request, 'The new password may not contain the '
                                    'username')
        elif form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your password was successfully updated!')

            return render(request, 'accounts/profile/display_profile.html',
                          {'user_profile': user_profile})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/profile/change_password.html', {
        'form': form
    })
