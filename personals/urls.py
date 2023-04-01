from django.urls import path
from personals import views

urlpatterns = [
    path('personals/', views.PersonalList.as_view()),
    path('personals/<int:pk>/', views.PersonalDetail.as_view()),
]
