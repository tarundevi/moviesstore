from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count 
from cart.models import Item
from movies.models import Movie, Review

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})
        
@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

@staff_member_required
def admin_dashboard(request):
    template_data = {}
    template_data['title'] = 'Admin Dashboard'
    users_with_purchases = (
        User.objects
        .filter(order__item__isnull=False)
        .annotate(total_movies=Sum('order__item__quantity'))
        .order_by('-total_movies')
    )

    most_purchased = (
        Movie.objects.annotate(total_purchased = Sum('item__quantity'))
        .filter(total_purchased__isnull=False)
        .order_by('-total_purchased')
    )

    most_reviewed = (
        Movie.objects.annotate(total_reviews= Count('review'))
        .filter(total_reviews__gt=0)
        .order_by('-total_reviews')
    )

    template_data['most_purchased'] = most_purchased
    template_data['most_reviewed'] =most_reviewed

    template_data['users'] = users_with_purchases
    return render(request, 'accounts/admin_dashboard.html',
        {'template_data': template_data})




