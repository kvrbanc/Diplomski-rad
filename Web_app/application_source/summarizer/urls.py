from django.urls import path
from . import views, api

app_name = 'summarizer'
urlpatterns = [
    path('', views.homepage_view, name='homepage1'),
    path('home/', views.homepage_view, name='homepage2'),
    path('summarizer/', views.summary_request_form_view, name='summary-form'),
    path('api/', views.api_view, name='api'),
    path('summarize', api.summary_computation, name='summary-computation')
]