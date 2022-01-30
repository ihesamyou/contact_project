from django.urls import path
from .views import ContactViews

urlpatterns = [
    path('', ContactViews.as_view()),
    path('<str:phone_get>', ContactViews.as_view()),
    path('patch/<str:phone_patch>', ContactViews.patch)
]