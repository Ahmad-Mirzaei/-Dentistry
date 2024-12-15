from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import (
    RegisterUserForm, LoginUserForm,
    PatientForm, EditeProfileForm,
    VerifyRegisterForm, RememberPasswordForm,
    ContactUsForm, ChangePasswordForm
)
from .models import CustomUser, Patient, Visit, ContactUs
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from apps.diseases.models import Disease
import utils
from django.http import HttpResponse


class RegisterUserView(View):
    template_name = 'accounts_app/register.html'

    def get(self, request):
        form = RegisterUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if not form.is_valid():
            messages.error(request, "اطلاعات وارد شده معتبر نمی باشد", 'danger')
            return render(request, self.template_name, {"form": form})
        
        data = form.cleaned_data
        active_code = utils.create_active_code(5)
        CustomUser.objects.create_user(
            name=data['name'],
            family=data['family'],
            mobile_number=data['mobile_number'],
            specialty=data['specialty'],
            password=data['password2'],
            active_code=active_code
        )
        utils.send_sms(data['mobile_number'], f'کد فعال سازی حساب کاربری شما {active_code} می باشد')
        request.session['user_session'] = {
            'active_code': str(active_code),
            'mobile_number': str(data['mobile_number']),
        }
        messages.success(request, 'اطلاعات شما با موفقیت ثبت شد. کد دریافتی را وارد کنید', 'success')
        return redirect('accounts:verify')

class VerifyUserView(View):
    template_name = 'accounts_app/verify_user.html'

    def get(self, request):
        form = VerifyRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = VerifyRegisterForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نامعتبر می باشند', 'danger')
            return render(request, self.template_name, {'form': form})  
        data = form.cleaned_data
        user_session = request.session.get('user_session')
        remember_password = user_session.get('remember_password', False)
        if data['active_code'] != user_session['active_code']:
            messages.error(request, 'کد دریافتی اشتباه می باشد', 'danger')            
        if not remember_password:
            user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user.is_active = True
            user.active_code = utils.create_active_code(5)
            user.save()
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد', 'success')
            return redirect('accounts:login')
        else:
            return redirect('accounts:change_password')

class LoginUserView(View):
    template_name = 'accounts_app/login.html'

    def get(self, request):
        form = LoginUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginUserForm(request.POST)
        if not form.is_valid():
            messages.warning(request, "اطلاعات وارد شده معتبر نمیباشد", 'warning')
            return render(request, self.template_name, {'form': form})            
        data = form.cleaned_data
        user = authenticate(username=data['mobile_number'], password=data['password'])
        if user is None:
            messages.warning(request, 'کاربر یافت نشد', 'warning')
            return render(request, self.template_name, {'form': form})
            
        login(request, user)
        messages.success(request, 'ورود با موفقیت انجام شد', 'success')
        return redirect('accounts:user_panel')
        
class RememberPasswordView(View):
    template_name = 'accounts_app/partials/remember_password.html'

    def get(self, request):
        form = RememberPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RememberPasswordForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'شماره موبایل وارد شده موجود نمی باشد', 'danger')
            return render(request, self.template_name, {'form': form})

        data = form.cleaned_data
        user = CustomUser.objects.get(mobile_number=data['mobile_number'])
        active_code = utils.create_active_code(5)
        user.active_code = active_code
        user.save()
        utils.send_sms(data['mobile_number'], f'کد تایید حساب کاربری شما {active_code} می باشد')
        request.session['user_session'] = {
            'active_code': str(active_code),
            'mobile_number': str(data['mobile_number']),
            'remember_password': True,
        }
        messages.success(request, 'جهت تغییر رمز عبور خود کد تایید را ارسال کنید', 'success')
        return redirect('accounts:verify')

class ChangePasswordView(View):
    template_name = 'accounts_app/partials/change_password.html'

    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده معتبر نمی باشد', 'danger')
            return render(request, self.template_name, {'form': form})
            
        data = form.cleaned_data
        user_session = request.session['user_session']
        user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
        user.set_password(data['password1'])
        user.active_code = utils.create_active_code(5)
        user.save()
        messages.success(request, 'رمز عبور شما با موفقعیت تغییر کرد', 'success')
        return redirect('accounts:login')

class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'خروج شما با موفقعیت انجام شد', 'success')
        return redirect('main:index')


class UserPanelView(View):
    template_name = 'accounts_app/userpanel.html'

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'لطفاً وارد شوید', 'danger')
            return redirect('accounts:login')
        
        dentist = CustomUser.objects.get(pk=request.user.id)
        return render(request, self.template_name, {'dentist': dentist})


class Patients(View):
    template_name = 'accounts_app/partials/patients.html'

    def get(self, request):
        # patients = Patient.objects.filter(is_active=True, dentist=request.user.id)
        return render(request, self.template_name)


class TablePatientsView(View):
    template_name = 'accounts_app/partials/table_patients.html'

    def get(self, request):
        patients = Patient.objects.filter(is_active=True, dentist=request.user.id)
        return render(request, self.template_name, {'patients': patients})



class EditProfileView(View):
    template_name = 'accounts_app/partials/edit_profile.html'

    def get(self, request):
        user = request.user
        data = {
            'mobile_number': user.mobile_number,
            'name': user.name,
            'family': user.family,
            'specialty': user.specialty,
            'email': user.email,
        }

        form = EditeProfileForm(initial=data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EditeProfileForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نامعتبراند', 'danger')
            return render(request, self.template_name, {'form': form}) 
        
        data = form.cleaned_data
        user = request.user
        user.mobile_number = data['mobile_number']
        user.name = data['name']
        user.family = data['family']
        user.email = data['email']
        user.specialty = data['specialty']
        user.save()
        messages.success(request, 'ویرایش پروفایل با موفقیت انجام شد', 'success')
        return redirect('accounts:user_panel')

class CreatePatient(View):
    template_name = 'accounts_app/partials/add_patient.html'

    def get(self, request):
        form = PatientForm()
        context = {
            'form': form,
            'diseases': Disease.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PatientForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نامعتبراند', 'danger')
            return render(request, self.template_name, {'form': form})
            
        data = form.cleaned_data
        diseases_ids = request.POST.getlist('diseases_id', [])
        patient = Patient.objects.create(
            name=data['name'],
            family=data['family'],
            phone_number=data['phone_number'],
            dentist=request.user,
            patient_national_id=data['patient_national_id'],
            is_active=data['is_active'],
        )
        visit = Visit.objects.create(
            patient=patient
        )
        visit.save()
        for disease in diseases_ids:
            patient.diseases.add(disease)
        patient.save()
        messages.success(request, 'اطلاعات بیمار با موفقیت ثبت شد', 'success')
        return redirect('diseases:part_blog', id=patient.id)

class UpdatePatient(View):
    template_name = 'accounts_app/partials/edit_patient.html'

    def get_all_diseases(self):
        return Disease.objects.all()

    def get(self, request, id):
        patient = get_object_or_404(Patient, pk=id)
        all_diseases = self.get_all_diseases()
        data = {
            'name': patient.name,
            'family': patient.family,
            'phone_number': patient.phone_number,
            'dentist': patient.dentist,
            'diseases': list(patient.diseases.all()),
            'patient_national_id': patient.patient_national_id,
            'is_active': patient.is_active,
        }

        form = PatientForm(initial=data)

        context = {'form': form, 'all_diseases': all_diseases,
                   'disease_selected_ids': list(patient.get_diseases().values_list('id', flat=True))}

        return render(request, self.template_name, context)

    def post(self, request, id):
        patient = get_object_or_404(Patient, pk=id)
        form = PatientForm(request.POST)
        all_diseases = self.get_all_diseases()

        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نامعتبر می باشند')
            return render(request, self.template_name, {'form': form, 'all_diseases': all_diseases})
            
        data = form.cleaned_data
        diseases_ids = request.POST.getlist('diseases_id', [])
        patient.name = data['name']
        patient.family = data['family']
        patient.phone_number = data['phone_number']
        patient.patient_national_id = data['patient_national_id']
        patient.is_active = data['is_active']
        patient.diseases.clear()
        patient.diseases.add(*diseases_ids)  # Use unpacking to add multiple diseases
        patient.save()
        visit = Visit.objects.create(
            patient=patient
        )
        visit.save()
        messages.success(request, 'اطلاعات بیمار با موفقیت ویرایش شد', 'success')
        return redirect('accounts:patients')

class ContactUsView(View):
    template_name = 'accounts_app/contact_us.html'

    def get(self, request):
        form = ContactUsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactUsForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نامعبراند', 'danger')
            return render(request, self.template_name, {'form': form})
        
        data = form.cleaned_data
        ContactUs.objects.create(
            fullname=data['fullname'],
            mobile_number=data['mobile_number'],
            subject=data['subject'],
            text=data['text'],
        )
        messages.success(request, 'پیام شما با موفقیت ارسال شد', 'success')
        return redirect('main:index')

class DeletePatientView(View):
    def get(self, request):
        patient_id = request.GET.get('patient_id')
        Patient.objects.get(id=patient_id).delete()
        return redirect('accounts:table_patients')

