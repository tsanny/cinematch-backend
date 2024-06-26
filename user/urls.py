from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
        MyTokenObtainPairView,
        RegisterView,
        getProfile,
        updateProfile,
)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),

    path('profile/', getProfile, name='profile'),
    path('profile/update/', updateProfile, name='update-profile'),

]
