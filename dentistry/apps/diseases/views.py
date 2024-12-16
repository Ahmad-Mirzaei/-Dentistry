from django.shortcuts import render
from .models import Disease
from django.views import View
from apps.accounts.models import Patient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

# Create your views here.

class BlogView(View):
    def get(self, request, *args, **kwargs):
        diseases = Disease.objects.filter(is_active=True).order_by('-is_priority')
        # آخرین محصولات
        last_diseases = Disease.objects.filter(is_active=True).order_by('-publication_date')[:3]

        # # Pagination
        # page_number = request.GET.get('page', 1)  # Get the current page number from the query parameters
        # paginator = Paginator(diseases, 2)  # Show 5 diseases per page
        
        # try:
        #     page_obj = paginator.page(page_number)
        # except PageNotAnInteger:
        #     page_obj = paginator.page(1)  # If page is not an integer, deliver first page.
        # except EmptyPage:
        #     page_obj = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page of results.
            
            
        # pager
       # تعداد مقاله در هر صفحه  
        product_per_page = 3  
        display_type = request.GET.get('display', product_per_page)  

        try:  
            display_type = int(display_type)  
        except (ValueError, TypeError):  
            display_type = product_per_page  # مقدار پیش فرض  

        paginator = Paginator(diseases, display_type)  
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number)  


        
        context = {
            'diseases': diseases,
            'last_diseases':last_diseases,
            'page_obj': page_obj,
            'current_display': display_type,
            }
        
        return render(request, 'diseases_app/blag.html', context)
    
    
def part_blog(request, id):
    patient = Patient.objects.get(pk=id)
    diseases_patient = patient.diseases.all()
    return render(request, 'diseases_app/part_blog.html', {'diseases_patient':diseases_patient})
      
      
class DetailBlogView(View):
    template_name = 'diseases_app/detail_blog.html'
    def get(self, request, id):
        disease = Disease.objects.get(is_active=True, pk=id)
        return render(request, self.template_name, {'disease':disease})
    
    
class ResultDescriptionView(View):  # بررسی نام کلاس  
    def get(self, request):  
        selected_values = request.GET.get('selected_values')  # دریافت مقادیر  
        print(selected_values)
        return JsonResponse({'selected_values': selected_values})  # بازگشت به صورت JSON 
    
    