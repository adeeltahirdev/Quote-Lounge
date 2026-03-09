# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import Profile
from .models import Quote, Category

User = get_user_model()



# -------------------- QUOTE VIEWS --------------------

def index(request):
    quote_list = Quote.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    current_category = request.GET.get('category', 'all')
    if current_category != 'all':
        quote_list = quote_list.filter(category__name=current_category)

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(quote_list, 6)  # 6 quotes per page
    page_number = request.GET.get('page')
    quotes = paginator.get_page(page_number)

    context = {
        'quotes': quotes,
        'categories': categories,
        'current_category': current_category,
        'total_quotes': Quote.objects.count(),
    }
    return render(request, 'index.html', context)


@login_required
def add_quote(request):
    if request.method == 'POST':
        text = request.POST.get('quotetext')
        author_name = request.POST.get('author')
        category_id = request.POST.get('category')

        category = Category.objects.get(id=category_id) if category_id else None

        Quote.objects.create(
            user=request.user,
            text=text,
            author_name=author_name,
            category=category
        )

        messages.success(request, 'Quote added successfully!')
        return redirect('index')

    categories = Category.objects.all()
    return render(request, 'quote/add_quote.html', {'categories': categories})

@login_required
def edit_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id, user=request.user)

    if request.method == 'POST':
        quote.text = request.POST.get('quotetext')
        quote.author_name = request.POST.get('author')
        category_id = request.POST.get('category')
        quote.category = Category.objects.get(id=category_id) if category_id else None

        quote.save()
        messages.success(request, 'Quote updated successfully!')
        return redirect('profile')

    categories = Category.objects.all()
    return render(request, 'quote/edit_quote.html', {'quote': quote, 'categories': categories})


@login_required
def like(request, q_id):
    quote = get_object_or_404(Quote, id=q_id)
    
    quote.likes_count += 1
    quote.save()
    
    return redirect('index')


@login_required
def delete(request, q_id):
    quote = get_object_or_404(Quote, id=q_id, user=request.user)
    quote.delete()
    messages.success(request, 'Quote deleted successfully!')
    return redirect('profile')