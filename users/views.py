from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, ChangePasswordForm
from django.contrib import messages
from .models import Profile



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

			#Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
            password=request.POST['password2'])
            login(request, authenticated_user)
            messages.success(request, f'{first_name} your account has been created successfully. Please setup your profile!')
            return redirect('users:edit_profile')

        else:
            first_name = form.data.get('first_name')
            last_name = form.data.get('last_name')
            username = form.data.get('username')
            email = form.data.get('email')
            password1 = form.data.get('password1')
            password2 = form.data.get('password2')
            messages.error(request, f'Unable to create the account! Please correct the errors below.')

    else:
        form = SignUpForm()
        first_name = ''
        last_name = ''
        username = ''
        email = ''
        password1 = ''
        password2 = ''


    context = {
       'form': form, 'first_name': first_name, 'last_name': last_name, 'username': username, 'email':email, 'password1': password1, 'password2': password2
    }

    return render(request, 'users/signup.html', context)

@login_required
def logout(request):
    django_logout(request)
    return render(request, 'users/logout.html')


@login_required
def profile(request, username=None):
    if username:# For other users
        user = get_object_or_404(User, username=username)
        profile = user.profile
    else:# For current user
        profile = request.user.profile

    context = {
    'profile': profile,
    }
    return render(request, 'users/profile.html', context)

@login_required
def report_profile(request, profile_id):
    """Report profile with JS"""
    if request.method =="POST":
        response_data= {}
        if Profile.objects.filter(id=profile_id).exists():
            profile = Profile.objects.get(id=profile_id)
            if profile.user != request.user:
                if profile.reported == False:
                    profile.reported = True
                    profile.save()
                    response_data['status'] = "reported"
                else:
                    profile.reported = False
                    profile.save()
                    response_data['status'] = "already_reported"
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def edit_profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Profile has been updated successfully.')
            return redirect('users:profile')
        else:
            messages.error(request, f' Unable to update profile. Please correct the error below.')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)


    context = {
       'uform': uform,
       'pform': pform
    }

    return render(request, 'users/edit_profile.html', context)


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            authenticated_user = authenticate(username=request.user.username,
            password=request.POST['new_password'])
            login(request, authenticated_user)
            messages.success(request, 'Your password has been updated successfully.')

            return redirect('users:change_password')
        else:
            messages.error(request, f'Unable to update the password! Please correct the errors below.')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
    'form':form,
    }

    return render(request, 'users/change_password.html', context)
