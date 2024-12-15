from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('register/',  views.RegisterUserView.as_view(), name='register'),
    path('verify/',  views.VerifyUserView.as_view(), name='verify'),
    path('logout/',  views.LogoutUserView.as_view(), name='logout'),
    path('contact_us/',  views.ContactUsView.as_view(), name='contact_us'),
    
    path('user_panel/',  views.UserPanelView.as_view(), name='user_panel'),
    path('edite_profile/',  views.EditProfileView.as_view(), name='edite_profile'),
    path('patients/',  views.Patients.as_view(), name='patients'),
    path('table_patients/',  views.TablePatientsView.as_view(), name='table_patients'),
    path('delete_patient/',  views.DeletePatientView.as_view(), name='delete_patient'),
    
    path('add_patients/',  views.CreatePatient.as_view(), name='add_patients'),
    path('edit_patient/<int:id>/',  views.UpdatePatient.as_view(), name='edit_patient'),
    path('remember_password/',  views.RememberPasswordView.as_view(), name='remember_password'),
    path('change_password/',  views.ChangePasswordView.as_view(), name='change_password'),  
]
