from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product
def add_to_cart(request,product_id):
    if request.method!='POST': 
        return redirect('products:home')
    
    p=get_object_or_404(Product,id=product_id,is_available=True); 
    cart=request.session.setdefault('cart',{}); 
    k=str(p.id)
    if p.stock<1: 
        messages.error(request,'Product is out of stock.'); 
        return redirect(p.get_absolute_url())
    
    if k in cart:
        if cart[k]['quantity']>=p.stock: messages.warning(request,'Maximum available stock reached.');
        return redirect('cart:detail')
        cart[k]['quantity']+=1
    else: 
        cart[k]={'name':p.name,'price':str(p.price),'quantity':1,'image':p.image.url if p.image else ''}
    request.session.modified=True; 
    messages.success(request,f'{p.name} added to cart.'); 
    return redirect('cart:detail')

def detail(request):
    cart=request.session.get('cart',{}); 
    items=[]; 
    total=Decimal('0')
    for pid,item in cart.items():
        sub=Decimal(item['price'])*item['quantity']; 
        total+=sub; 
        items.append({'product_id':pid,**item,'item_total':sub})
    return render(request,'cart/detail.html',{'items':items,'total':total})

def update(request,product_id):
    if request.method!='POST': return redirect('cart:detail')
    cart=request.session.get('cart',{}); k=str(product_id)
    if k in cart:
        p=get_object_or_404(Product,id=product_id)
        try: qty=int(request.POST.get('quantity',1))
        except (TypeError,ValueError): qty=1
        if qty<=0: cart.pop(k)
        else: cart[k]['quantity']=min(qty,p.stock)
        request.session.modified=True
    return redirect('cart:detail')
def remove(request,product_id):
    if request.method=='POST': request.session.get('cart',{}).pop(str(product_id),None); 
    request.session.modified=True; messages.info(request,'Item removed.')
    return redirect('cart:detail')
