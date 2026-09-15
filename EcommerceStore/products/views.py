from django.shortcuts import get_object_or_404, render
from .models import Category, Product
def home(request):
    products=Product.objects.filter(is_available=True,stock__gt=0).select_related('category')
    categories=Category.objects.all(); 
    category_slug=request.GET.get('category'); 
    query=request.GET.get('q','')
    if category_slug: 
        products=products.filter(category__slug=category_slug)
    if query: 
        products=products.filter(name__icontains=query)
    return render(request,'products/home.html',{'products':products,'categories':categories,'selected_category':category_slug,'query':query})

def detail(request,slug):
    product=get_object_or_404(Product,slug=slug,is_available=True)
    return render(request,'products/detail.html',{'product':product})
