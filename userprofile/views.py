from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
from .models import Userprofile
from django.utils.text import slugify
from django.contrib import messages
from django import forms

from store.forms import ProductForm
from store.models import Product, OrderItem, Order
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm



# Create your views here.
def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'products':products,
    })

@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    order_items = OrderItem.objects.filter(product__user=request.user)
    return render(request, 'userprofile/mystore.html',{
        'products': products,
        'order_items': order_items,
    })

@login_required
def my_store_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'userprofile/my_store_order_detail.html', {
        'order': order
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')

            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'The product was added!')

            return redirect('my_store')
    else:
        form = ProductForm()
    return render(request, 'userprofile/product_form.html',{
        'title':'Add Product', 'form':form
    })

@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'The changes was saved!')

            return redirect('my_store')
    else:
        form = ProductForm(instance=product)
    return render(request, 'userprofile/product_form.html', {
        'title': 'Edit product',
        'product': product,
        'form': form
    })

@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, 'The product was deleted!')

    return redirect('my_store')



@login_required
def myaccount(request):
    user = request.user
    return render(request, 'userprofile/myaccount.html')


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            # Create Userprofile object for the user
            userprofile = Userprofile.objects.create(user=user)
            # You may set additional fields for the userprofile here if needed
            userprofile.save()

            return redirect('frontpage')
    else:
        form = SignupForm()

    return render(request, 'userprofile/signup.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             userProfile = Userprofile.objects.create(user=user)
#             return redirect('frontpage')
#     else:
#         form = UserCreationForm()

#     return render(request, 'userprofile/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin:index')
                else:
                    return redirect('frontpage')
    else:
        form = AuthenticationForm()

    return render(request, 'userprofile/login.html', {'form': form})