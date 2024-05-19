from django.urls import path
from . import views


urlpatterns = [
    path('', views.scrap, name='scrap'),
    path('progress/<int:indicator>/', views.progress_bar, name='progress_bar'),
    path('lists/', views.data_list, name='navigation_lists'),
    path('cards/<int:id>/', views.business_card, name='business_card'),
]