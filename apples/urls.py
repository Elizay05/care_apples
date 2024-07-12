from django.urls import path
from . import views


urlpatterns = [
    #AUTH
    path('register_admin/', views.register_admin, name="register_admin"),
    path('register_user/', views.register_user, name="register_user"),
    path('login/', views.login, name="login"),

    #USER
    path('user_details/', views.user_details, name='user_details'),
    path('user/delete/<int:id>/', views.delete_user, name="delete_user"),

    #WOMEN
    path('register_women/', views.register_women, name='register_women'),
    path('edit_women/', views.edit_women, name='edit_women'),

    #MUNICIPALITIES
    path('municipalities/', views.municipalities, name="municipalities"),
    path('create_municipality/', views.create_municipality, name="create_municipality"),
    path('edit_municipality/<int:id>/', views.edit_municipality, name="edit_municipality"),
    path('municipality/delete/<int:id>/', views.delete_municipality, name="delete_municipality"),

    #ESTABLISHMENTS
    path('establishments/', views.establishments, name="establishments"),
    path('create_establishment/', views.create_establishment, name="create_establishment"),
    path('edit_establishment/<int:id>/', views.edit_establishment, name="edit_establishment"),
    path('establishment/delete/<int:id>/', views.delete_establishment, name="delete_establishment"),

    #CATEGORIES
    path('categories/', views.categories, name="categories"),
    path('create_category/', views.create_category, name="create_category"),
    path('edit_category/<int:id>/', views.edit_category, name="edit_category"),
    path('category/delete/<int:id>/', views.delete_category, name="delete_category"),

    #SERVICES
    path('services/', views.services, name="services"),
    path('create_service/', views.create_service, name="create_service"),
    path('edit_service/<int:id>/', views.edit_service, name="edit_service"),
    path('service/delete/<int:id>/', views.delete_service, name="delete_service"),

    #APPLES
    path('apples/', views.apples, name="apples"),
    path('create_apple/', views.create_apple, name="create_apple"),
    path('edit_apple/<int:id>/', views.edit_apple, name="edit_apple"),
    path('apple/delete/<int:id>/', views.delete_apple, name="delete_apple")
]