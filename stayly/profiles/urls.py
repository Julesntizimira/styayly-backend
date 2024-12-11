from django.urls import path
from .views import profiles, create_profile, profile_detail, login_user, test_token


urlpatterns = [
    path('', profiles, name='profiles'),
    path('create/', create_profile, name='create_profile'),
    path('delete/<str:pk>/', profile_detail, name='delete_profile'),
    path('update/<str:pk>/', profile_detail, name='update_profile'),
    path('get/<str:pk>/', profile_detail, name='get_profile'),
    path('login/', login_user, name='login_user'),
    path('test_token', test_token, name='test_token'),
]