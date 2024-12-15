from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from apps.accounts.models import CustomUser, Patient
from apps.diseases.models import Disease

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="رمز", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار رمز", widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'email', 'name', 'family', 'gender']

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن باهم مغایرت دارند')
        return pass2

    def save(self, commit=True):    # این تابع دوباره نویسی میشود به دلیل هش شدن پسورد
        user = super().save(commit=False)  # باعث می شود یوزر سیو نشود
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):  # وقتی میخواهیم کاربری را تغییر دهیم
    password = ReadOnlyPasswordHashField(help_text="<a href='../password'>تغییر رمز عبور </a>")
    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin']
        
# ورود کاربر
class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' موبایل را وارد کنید'})
                                )
    password = forms.CharField(label='رمز عبور',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' رمز عبور را وارد کنید'})
                                )


# ثبت نام کاربر
class RegisterUserForm(forms.ModelForm):    # ایجاد فرمی برای ثبت نام کاربرای در سایت
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور را وارد کنید'}))
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور را وارد کنید'}))
    class Meta:
        model = CustomUser
        fields = ['mobile_number', 'name', 'family', 'specialty']
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موبایل را وارد کنید'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام را وارد کنید'}),
            'family': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی را وارد کنید'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تخصص را وارد کنید'}),
        }

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن باهم مغایرت دارند')
        return pass2
    
# احراز
class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد دریافتی را وارد کنید'})
                                )
        
# ویرایش پروفایل
class EditeProfileForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' موبایل را وارد کنید'})
                                )
    
    name = forms.CharField(label='نام',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' نام را وارد کنید'})
                                )
    
    family = forms.CharField(label='نام خانوادگی',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' نام خانوادگی را وارد کنید'})
                                )
    
    email = forms.CharField(label='ایمیل',
                                required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل را وارد کنید'})
                                )
    
    specialty = forms.CharField(label='تخصص',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تخصص را وارد کنید'})
                                )

        
# نمایش و اضافه کردن بیماران
class PatientForm(forms.ModelForm):
    diseases = forms.ModelMultipleChoiceField(
        queryset=Disease.objects.filter(is_active=True).order_by('-is_priority'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="بیماری ها"
        )
    class Meta:
        model = Patient
        fields = ['name', 'family', 'phone_number','patient_national_id', 'is_active', 'diseases']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام را وارد کنید'}),
            'family': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی را وارد کنید'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موبایل را وارد کنید'}),
            'patient_national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد ملی را وارد کنید'}),
            # 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  
            # 'diseases': forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
        }


# تایید شماره موبایل 
class RememberPasswordForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل',
                                    error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'شماره موبایل را وارد کنید'}),
                                    )
    
# تغییر رمز
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='رمز عبور',
                            error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' رمز عبور را وارد کنید'})
                            )
    password2 = forms.CharField(label='رمز عبور',
                        error_messages={'required': 'این فیلد نمی تواند خالی باشد'},
                        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' تکرار رمز عبور را وارد کنید'})
                        )
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن باهم مغایرت دارند')
        return pass2
    
class ContactUsForm(forms.Form):
    fullname = forms.CharField(label='نام و نام خانوادگی' ,
                        max_length=100,
                        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"نام و نام خانوادگی خود را وارد کنید"})
                        )
    mobile_number = forms.CharField(label='شماره موبایل',
                        max_length=20,
                        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":" شماره موبایل خود را وارد کنید"})
                        )
    subject = forms.CharField(label='موضوع',
                        max_length=50,
                        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"موضوع خود را وارد کنید"}),
                        required=False
                        )
    text = forms.CharField(label='پیام',
                        max_length=100,
                        widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"پیام خود را وارد کنید", 'rows':4}),
                        )