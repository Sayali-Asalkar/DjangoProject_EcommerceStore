from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem
@login_required
def checkout(request):
    cart=request.session.get('cart',{})
    if not cart: 
        messages.warning(request,'Your cart is empty.'); 
        return redirect('cart:detail')
    
    total=sum(Decimal(x['price'])*x['quantity'] for x in cart.values());
    form=CheckoutForm(request.POST or None,initial={'full_name':request.user.get_full_name(),'email':request.user.email} if request.method=='GET' else None)
    if request.method=='POST' and form.is_valid():
        try:
            with transaction.atomic():
                for pid,item in cart.items():
                    p=Product.objects.select_for_update().get(id=pid)
                    if item['quantity']>p.stock: raise ValueError(p.name)
                order=form.save(commit=False);
                order.user=request.user; 
                order.total_amount=total; 
                order.save()

                for pid,item in cart.items():
                    p=Product.objects.get(id=pid); 
                    OrderItem.objects.create(order=order,product_name=p.name,price=Decimal(item['price']),quantity=item['quantity']); 
                    p.stock-=item['quantity']; 
                    p.is_available=p.stock>0; 
                    p.save(update_fields=['stock','is_available'])
        except ValueError as e: messages.error(request,f'Not enough stock for {e.args[0]}.'); 
        return redirect('cart:detail')
        request.session['cart']={}; messages.success(request,f'Order #{order.id} placed successfully.'); return redirect('orders:success',order_id=order.id)
    return render(request,'orders/checkout.html',{'form':form,'total':total})
@login_required
def success(request,order_id): 
    return render(request,'orders/success.html',{'order':get_object_or_404(Order,id=order_id,user=request.user)})
@login_required
def history(request): 
    return render(request,'orders/history.html',{'orders':Order.objects.filter(user=request.user)})
