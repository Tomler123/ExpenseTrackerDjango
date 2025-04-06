from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Book
from .forms import CategoryForm, BookForm

# Create your views here.
# Create Categories
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    
    else:
        form = CategoryForm()
    return render(request, 'books/category_form.html', {'form': form})

# List Categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'books/category_list.html', {'categories': categories})

# Update Category
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()  # This will automatically handle the `full_clean()`
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'books/category_form.html', {'form': form, 'category': category})

# Delete Category
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'books/category_confirm_delete.html', {'category':category})

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form':form})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books':books})

def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/book_form.html', {'form':form, 'book':book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book':book})