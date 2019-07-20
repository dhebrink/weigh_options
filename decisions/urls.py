from django.urls import path


from . import views

app_name = 'decisions'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:template_id>/', views.preview, name='preview'),
    path('copy/', views.copy, name='copy'),
    path('fill_form/<int:copy_id>/', views.fill_form, name='fill_form'),
    path('save/', views.save_copy, name='save_copy')
]
