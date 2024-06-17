from django.contrib import admin
from blogs.models import BlogModel, BlogTagModel, BlogCategoryModel, BlogCommentModel


@admin.register(BlogCategoryModel)
class BlogCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'created_at')
    list_filter = ('name', 'created_at')




@admin.register(BlogTagModel)
class BlogTagModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'created_at')
    list_filter = ('name', 'created_at')



@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'created_at')
    list_filter = ('created_at',)

@admin.register(BlogCommentModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')
    search_fields = ('user', 'created_at')
    list_filter = ('created_at',)


