from django.contrib import admin
from .models import Disease
# Register your models here.

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_priority','is_active','get_shamsi_date']
    list_filter = ['title', 'is_priority', 'is_active']
    search_fields = ('title',)
    ordering = ('publication_date',)
    list_editable = ['is_priority', 'is_active']
    
    class Media:
        css = {
            'all': ('css/admin_style.css',)
        }
        
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',
        )
