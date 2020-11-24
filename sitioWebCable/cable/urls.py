from django.urls import path

from . import views
app_name = 'cable'
urlpatterns = [
    path('', views.mainView.as_view(), name='main'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', views.logoutView.as_view(), name='logout'),
    path('crearUsuarios/', views.createUser, name='crearUsuarios'),
    path('crearCatalogo/', views.createCatalogo, name='crearCatalogo'),
]