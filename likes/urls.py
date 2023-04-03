# Third party imports
from django.urls import path

# Internal imports
from likes import views

urlpatterns = [
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>', views.LikeDetail.as_view()),
]
