from django.contrib import admin
from .models import Category, Idea ,LegalDocument

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_official_product', 'created_at')
    list_filter = ('is_official_product', 'category')
    search_fields = ('title', 'description')


admin.site.register(LegalDocument)