from django.contrib import admin

# Register your models here.
from .models import (
    Answer, Category, Prompt, SubCategory, Template, TemplateCopy,
)


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 2


class AdminCategory(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['name']
    inlines = [SubCategoryInline]


class PromptInline(admin.TabularInline):
    model = Prompt
    extra = 5
    fields = ['text', 'description', 'answer_type', 'answer_options']


class AdminTemplate(admin.ModelAdmin):
    fields = ['name']
    search_fields = ['name']
    inlines = [PromptInline]


admin.site.register(Category, AdminCategory)
admin.site.register(Template, AdminTemplate)
