"""
URL configuration for djangoConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from user import views
from rest_framework import routers




# define the router
router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('register/', views.Registration_view.as_view(), name='register'),
    path('friend_request/', views.FriendRequestHandle_view.as_view(), name='friend_request'),
    path('friend_request_list/', views.FriendList_view.as_view(), name='friend_request_list'),
    path('friend_request_pending_list/', views.PendingFriendList_view.as_view(), name='friend_request_pending'),
    path('user_search/', views.UserSearchView.as_view(), name='friend_search'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')) # Adds 'Login' link in the top right of the page

]