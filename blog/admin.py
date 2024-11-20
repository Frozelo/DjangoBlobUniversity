from django.contrib import admin
from django.utils.html import format_html
from .models import Categorie, Tag, Post, PostTagRelation


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('slug',)
    ordering = ('title',)
    list_editable = ('slug',)
    list_display_links = ('title',)

    fields = ('title', 'slug')

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = obj.title.lower().replace(' ', '-')
        super().save_model(request, obj, form, change)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('slug',)
    ordering = ('title',)
    list_editable = ('slug',)
    list_display_links = ('title',)

    def save_mode(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = obj.title.lower().replace(' ', '-')
        super().save_model(request, obj, form, change)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'thumbnail_display', 'views')
    prepopulated_fields = {'slug': ('title',)}


    def thumbnail_display(self, obj):
        if obj.thumbnail:
            print(obj.thumbnail.url)
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.thumbnail.url)
        return "Нет изображения"

    thumbnail_display.short_description = 'Thumbnail'

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = obj.title.lower().replace(' ', '-')
        super().save_model(request, obj, form, change)


admin.site.register(Categorie, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostTagRelation)
