from django.db import models                            #(کلاسی برای سطح دسترسی ها)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager, UserManager
from django.utils import timezone
from apps.diseases.models import Disease
from jalali_date import datetime2jalali
# Create your models here.

# نوشتن کلاسی برای مدیریت کاربران :
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, specialty, email="", name="", family="", active_code=None, gender=None, password=None):
        if not mobile_number:
            raise ValueError("شماره موبایل باید وارد شود")
        
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email), # تابعی که فرمت دهی ایمیل را چک و صحیح میکند
            name= name,
            family=family,
            specialty=specialty,
            gender=gender,
            active_code=active_code,    
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # >>creatsuperuser وقتی این دستور زده میشود این تابع اجرا میشود : 
    def create_superuser(self, mobile_number, email, name, family, password=None, active_code=None, gender=None, specialty=None):
        user=self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password,
            specialty=specialty
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    email = models.EmailField(max_length=200, blank=True, verbose_name='ایمیل')
    name = models.CharField(max_length=50, blank=True, verbose_name='نام')
    family = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی')
    specialty = models.CharField(max_length=50,null=True, blank=True, verbose_name='تخصص')
    GENDER_CHOICES = (('True', 'مرد'), ('False', 'زن'))
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='True', blank=True, null=True, verbose_name='جنسیت')
    register_date = models.DateField(auto_now_add=True, verbose_name='تاریخ درج')
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    active_code = models.CharField(max_length=100, null=True, blank=True, verbose_name='کد احراز')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')

    USERNAME_FIELD = 'mobile_number' #مشخص کردن فیلد یوزر نام 
    REQUIRED_FIELDS = ['email','name','family']    # سوال هایی که برای ساختن سوپر یوزر باید پرسیده شوند
        # دوتا سوالی که به صورت پیش فرض پرسیده میشوند (موبایل و پسوود)
    
    objects = CustomUserManager() # نمونه ای از کلاس منیجر و کوِئری هایی که می نویسیم برای واکشی 
    
    def __str__(self):
        return self.name+" "+self.family
    
    @property
    def is_staff(self): # تعیین میکند که اگر کاربری این مقدارش ترو باشد بتواند به پنل دسترسی داشته باشد
        return self.is_admin
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Patient(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='نام')
    family = models.CharField(max_length=50, null=True, blank=True, verbose_name='نام خانوادگی')
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره موبایل')
    dentist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='self_dentist', verbose_name='دندانپزشک مریض')
    diseases = models.ManyToManyField(Disease, related_name='patients', verbose_name='بیماری ها')  # نوع بیماری  
    patient_national_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='کد ملی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return f"{self.name} {self.family}"

    def get_diseases(self):
        return self.diseases.all()
    
    class Meta:
        verbose_name = 'بیمار'
        verbose_name_plural = 'بیمار ها' 
        
class Visit(models.Model):  
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ مراجعه')

    def get_shamsi_date_visit(self):
        return f"{datetime2jalali(self.visit_date).strftime('%H:%M:%S__%y/%m/%d')}"
    
    def __str__(self):
        return self.visit_date
    
class ContactUs(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    mobile_number = models.CharField(max_length=50, verbose_name='شماره موبایل')
    subject = models.CharField(max_length=50, null=True, blank=True, verbose_name='موضوع')
    text = models.TextField(verbose_name='پیام')
    register_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ')

    def get_shamsi_date_contact(self):
        return datetime2jalali(self.register_date).strftime('%H:%M:%S _ %y/%m/%d')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'