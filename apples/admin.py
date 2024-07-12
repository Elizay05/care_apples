from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Municipality, Establishment, Category, Service, Apple, AppleService, User, Women

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'role', 'is_staff', 'is_superuser', 'profile_picture')

@admin.register(Women)
class CustomWomenAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'identification_number', 'name', 'phone', 'city', 'direction', 'ocupation')

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'image']

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "responsible", "direction", "image"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "image"]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "description",     "category", "establishment", "image"]

@admin.register(Apple)
class AppleAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "direction", "municipality", "list_services"]

@admin.register(AppleService)
class AppleServiceAdmin(admin.ModelAdmin):
    list_display = ["apple", "service"]
