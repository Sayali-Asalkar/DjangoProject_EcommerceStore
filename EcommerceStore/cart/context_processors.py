def cart(request):
    data=request.session.get('cart',{}); return {'cart_count':sum(x['quantity'] for x in data.values())}
