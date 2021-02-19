from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from accounts.models import MyUser
from django.http import HttpResponseRedirect
from .models import Mentee_Profile
# from doctor.models import appointments,Doctor_profile
# from hospital.models import Hospital_profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout
import uuid


# Create your views here.
def role_test(user):
    if user.role == "mentee":
        return True
    else:
        return False


@login_required(login_url='/login/')
@user_passes_test(role_test, login_url='/login/')
def mentee_view(request, id):
    # obj = Mentee_Profile.objects.filter(mentee_id=id)
    obj = MyUser.objects.filter(id=id)
    # obj = accounts_myuser.objects.filter(mentee_id=id)
    # obj= accounts_myuser.objects.filter(id)
    if obj:
        profile = list(MyUser.objects.filter(id=id).values('id', 'email'))
        name = MyUser.objects.filter(id=id)[0].fname


        roles=MyUser.objects.filter(role='Mentor').values('fname')

        profile_add = list(MyUser.objects.filter(id=id).values())
        print("heyyyyyyy")
        return render(request, 'Mentee_Profile.html',
                      {'profile': profile, 'profile_add': profile_add, "Profile_Name": name, 'mentor': roles})
    else:
        return redirect(f'/editMentee/{id}')


@login_required(login_url='/login/')
@user_passes_test(role_test, login_url='/login/')
def editMentee(request, id):
    # profile = list(MyUser.objects.filter(id=id).values('email'))
    # profile_add = list(MyUser.objects.filter(id=id).values())
    #
    if request.method == "POST":
        address = request.POST.get('address')
        picture = request.POST.get('profilepic')
    #obj = MyUser.objects.filter(id=id)
    # return render(request, 'Mentee_Profile.html',
    #               {'profile_addrs': address, 'testing': picture})
        request.session['testing']=picture
        request.session['profile_addrs']=address
        return redirect(request.path)
    else :
        address = request.POST.get('address')
        picture = request.POST.get('profilepic')
        # obj = MyUser.objects.filter(id=id)
        # return render(request, 'Mentee_Profile.html',
        #               {'profile_addrs': address, 'testing': picture})
        request.session['testing'] = picture
        request.session['profile_addrs'] = address
        # return redirect(request.path)
        return render(request, 'mentee_edit.html',
                      {'testing': 'No input', 'profile_addrs': 'no input'})
    # return HttpResponseRedirect('/',
    #               {'profile_addrs': address, 'testing': picture}
    #  if not obj:
    #     pt_obj = MyUser.objects.filter(id=id)
    #     pt_obj.pic = picture
    #     pt_obj.save()
    #     messages.success(request, 'success', {'testing': address})
    #     return redirect(f'/mentee/{id}/')
    # else:
    #     pt_obj = MyUser.objects.filter(id=id)
    #     pt_obj.pic = picture
    #     pt_obj.save()
    #     messages.success(request, 'successfully updated pic', {'testing': address})
    #     return redirect(f'/mentee/{id}/')
    # return render(request, 'mentee_edit.html',
    #               {'profile': profile, 'profile_add': profile_add, 'title': 'Edit Profile', 'testing': address})

def showmentee(request):
    return render(request, 'mentee_profile.html')
@login_required(login_url='/login/')
@user_passes_test(role_test, login_url='/login/')
def passwordChange(request, id):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            logout(request)
            messages.success(request, 'changed')
            return redirect(f'/accounts/login/')
        else:
            logout(request)
            messages.error(request, 'error')
            return redirect(f'/accounts/login/')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form, 'title': 'Change Password'})
@login_required(login_url='/login/')
def getwatingappointments(request, id):
    check = request.GET.get('type')
    if check == 'waiting':
        obj = list(appointments.objects.filter(mentee_id=id, is_confirmed=False, is_rejected=False,
                                               is_disabled=False).values())
    elif check == 'upcoming':
        obj = list(
            appointments.objects.filter(mentee_id=id, is_confirmed=True, is_rejected=False, is_disabled=False).values())
    elif check == 'completed':
        obj = list(
            appointments.objects.filter(mentee_id=id, is_completed=True, is_rejected=False, is_disabled=False).values())
    elif check == 'rejected':
        obj = list(appointments.objects.filter(mentee_id=id, is_rejected=True, is_disabled=False).values())
    else:
        return JsonResponse([], safe=False)
    if obj:

        for item in obj:
            doc_obj = list(Doctor_profile.objects.filter(id=item.get('doctor_id')).values())[0]
            hos_obj = list(Hospital_profile.objects.filter(id=doc_obj.get('hospital_id')).values())[0]
            item['doctor_name'] = doc_obj.get('name')
            item['doctor_qualification'] = doc_obj.get('qualification')
            item['doctor_speciality'] = doc_obj.get('speciality')
            item['hospital_name'] = hos_obj.get('name')
    return JsonResponse(obj, safe=False)
def get_list(request, id):
    doc_count = Doctor_profile.objects.filter(is_available=True).count()
    completed = appointments.objects.filter(mentee_id=id, is_completed=True, is_rejected=False,
                                            is_disabled=False).count()
    upcoming = appointments.objects.filter(mentee_id=id, is_confirmed=True, is_rejected=False,
                                           is_disabled=False).count()
    waiting = appointments.objects.filter(mentee_id=id, is_confirmed=False, is_rejected=False,
                                          is_disabled=False).count()
    rejected = appointments.objects.filter(mentee_id=id, is_rejected=True, is_disabled=False).count()
    return JsonResponse([doc_count, completed, upcoming, waiting, rejected], safe=False)
