from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, User
import bcrypt

# log in and registration


def landing(request):
    return render(request, 'landing.html')

# registration


def register(request):
    if request.method == "GET":
        return redirect("/landing.html")
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)
        user1 = User.objects.filter(email=request.POST['email'])
        if user1.exists():
            messages.error(request, "This email is already Registered!", extra_tags='register')
            return redirect('/')

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            user1 = User.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                password=bcrypt.hashpw(
                    request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['log_user_id'] = user1.id
        return redirect('/books')

    return redirect("/")
# login


def login(request):
    user_list = User.objects.filter(email=request.POST['email'])
    if user_list:
        logged_user = user_list[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['log_user_id'] = logged_user.id

            return redirect('/books')
        else:
            messages.error(request, "Invalid email or password.",
                           extra_tags='login')
            return redirect('/')
    messages.error(request, "Email does not exist.", extra_tags='login')
    return redirect('/')

# logout


def logout(request):
    request.session.clear()
    return redirect('/')


# Success Page/ User View
def books(request):

    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'user_books': Book.objects.all(),
        # 'liked_books':Book.user_favorites.through.objects.get(id=request.session['log_user_id']),
    }
    return render(request, 'books.html', context)

# adding a book


def add_book(request):
    if request.method == 'POST':
        errors1 = Book.objects.book_validator(request.POST)
        if len(errors1) > 0:
            for key, value in errors1.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/books')

        else:
            Book.objects.create(
                title=request.POST['title'],
                desc=request.POST['desc'],
                uploaded_by=User.objects.get(
                    id=request.session['log_user_id']),
            )
            user = request.session['log_user_id']
            add_fav = Book.objects.last()
            if add_fav.user_favorites.filter(id=user).exists():
                add_fav.user_favorites.remove(user)
            else:
                add_fav.user_favorites.add(user)
        return redirect('/books')

# add to Favorites


def favorite(request, id):
    user = request.session['log_user_id']
    add_fav = Book.objects.get(id=id)
    if add_fav.user_favorites.filter(id=user).exists():
        add_fav.user_favorites.remove(user)
    else:
        add_fav.user_favorites.add(user)
    return redirect('/books')

# details page without access to editing


def details(request, id):
    this_book = Book.objects.get(id=id)
    detail_query = {
        'books': this_book,
        'user': User.objects.get(id=request.session['log_user_id']),
        'liked':this_book.user_favorites.all()
        # 'liked': Book.user_favorites.through.objects.exclude(id=request.session['log_user_id']),

    }
    return render(request, 'details.html', detail_query)

    # Edit a book


def edit(request, id):
    edit_query = {
        'books': Book.objects.get(id=id),
        'user': User.objects.get(id=request.session['log_user_id']),
        'liked': Book.user_favorites.through.objects.exclude(id=request.session['log_user_id']),
    }
    return render(request, 'uploaded_book_detail.html', edit_query)

# showing only favorites of a user


def my_favs(request):
    my_favs_query = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'user_books': Book.objects.all(),
        'liked_books': Book.user_favorites.through.objects.get(id=request.session['log_user_id']),

    }
    return render(request, 'my_favorites.html', my_favs_query)

# update a Book function


def update(request, id):
    if request.method == 'POST':
        errors1 = Book.objects.book_validator(request.POST)
        if len(errors1) > 0:
            for key, value in errors1.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/edit/{id}')
        else:
            update = Book.objects.get(id=id)
            update.title = request.POST['title']
            update.desc = request.POST['desc']
            update.save()
            messages.success(
                request, 'Book Description Updated', extra_tags='update')
        return redirect('/books')

# to Delete a book


def destroy(request, id):
    if request.method == "POST":
        messages.warning(
            request, "Are you sure you want to delete this book :{books.title}?")
        dele = Book.objects.get(id=id)
        dele.delete()
    return redirect('/books')
