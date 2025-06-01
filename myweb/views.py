import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Bookmark, Category, Recipe


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not email:
            return render(request, 'register.html', {'messages': ['Username and Email are required.']})
        if password != password2:
            return render(request, 'register.html', {'messages': ['Passwords do not match.']})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
        except Exception as e:
            return render(request, 'register.html', {'messages': [f'Error: {str(e)}']})

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required
def bookmarked_recipes(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'bookmarked_recipes.html', {'bookmarks': bookmarks})

@login_required
def toggle_bookmark(request, recipe_id):
    if request.method == "POST" and request.user.is_authenticated:
        recipe = Recipe.objects.get(id=recipe_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, recipe=recipe)
        if not created:
            bookmark.delete()
            return JsonResponse({"bookmarked": False})
        return JsonResponse({"bookmarked": True})
    return JsonResponse({"error": "Unauthorized"}, status=401)


def static_recipe_detail(request, slug):
    static_path = os.path.join(settings.STATIC_URL, 'static_recipes', f'{slug}.html')
    return redirect(static_path)


def recipes(request):
    # Fetch all categories along with their related recipes
    categories = Category.objects.prefetch_related('recipes').all()
    recipes = Recipe.objects.all()

    # Get user's bookmarked recipes if authenticated
    user_bookmarks = Bookmark.objects.filter(user=request.user) if request.user.is_authenticated else []
    bookmarked_recipe_ids = [bookmark.recipe.id for bookmark in user_bookmarks]

    # Render the index.html template with categorized recipes and bookmark data
    return render(request, 'recipes/recipes.html', {
        'recipes': recipes,
        'categories': categories,
        'bookmarked_recipe_ids': bookmarked_recipe_ids,
    })

def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'aboutus.html')
