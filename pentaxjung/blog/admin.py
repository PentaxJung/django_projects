from django.contrib import admin

from .models import *

@admin.register(Entries)
class EntriesAdmin(admin.ModelAdmin):
	list_display = ['id', 'created', 'updated', 'Category', 'Title', 'Comments']

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
	list_display = ['Title']

@admin.register(TagModel)
class TagmodelAdmin(admin.ModelAdmin):
	list_display = ['Title']

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
	list_display = ['id', 'Name', 'Password', 'Content', 'created', 'Entry']