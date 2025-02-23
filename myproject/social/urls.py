

from django.urls import path
from . import views



urlpatterns = [
    path('home/',views.PostList.as_view(),name='home'),
    path('',views.PostList.as_view(),name='home'),
    path('create/',views.PostCreateView.as_view(),name='create_post'),
    path('update/<int:id>/',views.PostUpdateView.as_view(),name='update_post'),
    path('delete/<int:id>/',views.PostDeleteView.as_view(),name='delete_post'),

    path('signup/',views.signup,name='signup'),
    path('login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='user_logout'),
    path('profile/',views.user_profile,name='user_profile'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    
    # path('profile/',views.profile,name='profile'),
    
]
