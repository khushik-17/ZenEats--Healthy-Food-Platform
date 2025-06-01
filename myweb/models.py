from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    MEALS = 'Meals'
    SWEETS_AND_DESSERTS = 'Sweets and Desserts'
    SNACKS = 'Snacks'

    CATEGORY_CHOICES = [
        (MEALS, 'Meals'),
        (SWEETS_AND_DESSERTS, 'Sweets and Desserts'),
        (SNACKS, 'Snacks'),
    ]

    name = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=MEALS  # default category if no category is selected
    )

    def __str__(self):
        return self.get_name_display()  # Display human-readable category name
    
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/')
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE, related_name='recipes') # Add ForeignKey or ManyToManyField
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"

    class Meta:
        unique_together = ('user', 'recipe')  # Prevent duplicate bookmarks

