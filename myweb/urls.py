from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
     path("", views.home, name="home"),  # Updated index to home
    path("recipes/", views.recipes, name="recipes"),  # Recipes page
    path("recipes/<slug:slug>/", views.static_recipe_detail, name="static_recipe_detail"),
    path("bookmarked/", views.bookmarked_recipes, name="bookmarked_recipes"),
    path("toggle_bookmark/<int:recipe_id>/", views.toggle_bookmark, name="toggle_bookmark"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("aboutus/", views.aboutus, name="aboutus"),  # About Us page
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)