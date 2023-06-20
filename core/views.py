from django.shortcuts import render, redirect
from store.models import Product
from django.core.paginator import Paginator
from .forms import ContactForm
from .models import Contact

# Create your views here.

def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE)
    paginator = Paginator(products, 6)
    pageNumber = request.GET.get('page')
    frontData = paginator.get_page(pageNumber)
    totalPage = frontData.paginator.num_pages
    return render(request, 'core/frontpage.html', {'frontData':frontData, 'totalPage':totalPage, 'listofPages':[n+1 for n in range(totalPage)]})

def about(request):
    return render(request, 'core/about.html')



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            Contact.objects.create(name=name, email=email, message=message)
            return redirect('contact') 
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
