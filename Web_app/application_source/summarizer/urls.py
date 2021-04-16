from django.urls import path
from . import views, api

app_name = 'summarizer'
urlpatterns = [
    path('', views.homepage_view, name='homepage1'),
    path('home/', views.homepage_view, name='homepage2'),
    path('summarizer/', views.summary_request_form_view, name='summary-form'),
    path('api/', views.api_view, name='api'),
    path('summarize', api.summary_computation, name='summary-computation')
    # path('requests/', views.summaryRequestListView, name='summary_request_list'),
    # path('requests/<int:pk>/', views.RequestDetailView.as_view(), name='summary_request_detail'),
    # path('request-form/', views.summaryRequestFormView, name='summary_request_form')
]