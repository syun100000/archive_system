from django.urls import path
from . import views
from . import search

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path('search_page/', views.search_page, name='search_page'),
    path('search/', views.search, name='search'),
    path("upload_contents_detail/<int:id>/", views.upload_contents_detail, name="upload_contents_detail"),
    path("report_contents_detail/<int:id>/", views.report_contents_detail, name="report_contents_detail"),
    path('announcements/<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path("announcements/", views.announcements_list, name="announcements_list"),
    path('categories/', views.category_list, name='category'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
]
