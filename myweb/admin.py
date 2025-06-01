from django.contrib import admin
from .models import Recipe, Bookmark, Category

# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Assuming 'name' is the field for the category name

# Register the Recipe model and include the Category field
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "created_at")  # Added category to display  
    list_filter = ("category",)  # Add filter by category in the admin interface

# Register the Bookmark model
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe","created_at")
    list_filter = ("created_at",)
