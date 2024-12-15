from django.db import models
from django.utils import timezone
from jalali_date import datetime2jalali, date2jalali
# <<<<<<< HEAD
from ckeditor_uploader.fields import RichTextUploadingField
# =======


# >>>>>>> 8fa691a79f39a50af71c2b8b87149163ec7b0751
# Create your models here.

class Disease(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان بیماری')
    summary_description = models.TextField(max_length=100, default="", null=True, blank=True, verbose_name='خلاصه شرح')
    description = RichTextUploadingField(config_name='special',blank=True, null=True, verbose_name='توضیحات کامل')
    is_priority = models.BooleanField(default=False, verbose_name='اولویت بودن / نبودن')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن / نبودن')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    
    def get_shamsi_date(self):
        return datetime2jalali(self.publication_date).strftime('%H:%M:%S _ %y/%m/%d')
    
    get_shamsi_date.short_description = 'تاریخ درج'

    def __str__(self):
        return self.title
# <<<<<<< HEAD
        
    class Meta:
        verbose_name = 'بیماری'
        verbose_name_plural = 'بیماری ها'
        


# >>>>>>> 8fa691a79f39a50af71c2b8b87149163ec7b0751
