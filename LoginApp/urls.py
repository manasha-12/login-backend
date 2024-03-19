from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
)

urlpatterns = [
    path('', views.GetRoute, name='get-route'),
    path('user/login', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/profile', views.GetUserProfile, name='get_user_profile'),
    path('users', views.GetUsers, name='get_users'),
    path('user/register', views.RegisterUser, name='register_user'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    # path('user/activity-log', views.UserActivity, name='activity-log'),
    path('addProduct', views.PostProduct, name='add_product'),
    path('products', views.GetProducts, name="get_all_products"),
    # path('product/<int:id>', views.GetSingleProduct, name='single_product'),
]