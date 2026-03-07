from django.contrib import admin
from .models import User, Category, Subscription
from listing.models import announcement, AIGeneration
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'img')
    search_fields = ('title',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'expires_at', 'created_at')
    list_filter = ('plan',)
    search_fields = ('user__username', 'plan')

@admin.register(announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'created_at')
    search_fields = ('title', 'city')
    list_filter = ('city',)

@admin.register(AIGeneration)
class AIGenerationAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'created_at')
    search_fields = ('user__username', 'listing__title')
    list_filter = ('created_at',)