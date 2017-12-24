from django.shortcuts import render, HttpResponse, redirect

def index(request):
    context = {
        'somekey' : "somevalue"
    }
    return render(request, "amadon/index.html", context)

def buy(request):
    request.session.get('product_id', 0)
    request.session.get('price', 0)
    request.session.get('totalorders', 0)
    request.session.get('totalamount', 0)
    request.session['product_id'] = request.POST['product_id']
    if (request.POST['product_id'] == '1000'):
        request.session['price'] = 19.99 * int(request.POST['quantity'])
        request.session['totalorders'] = request.session['totalorders']+int(request.POST['quantity'])
        request.session['totalamount'] = request.session['totalamount'] + request.session['price']
    elif (request.POST['product_id'] == '1001'):
        request.session['price'] = 29.99 * int(request.POST['quantity'])
        request.session['totalorders'] = request.session['totalorders']+int(request.POST['quantity'])
        request.session['totalamount'] = request.session['totalamount'] + request.session['price']
    elif (request.POST['product_id'] == '1002'):
        request.session['price'] = 4.99 * int(request.POST['quantity'])
        request.session['totalorders'] = request.session['totalorders']+int(request.POST['quantity'])
        request.session['totalamount'] = request.session['totalamount'] + request.session['price']
    elif (request.POST['product_id'] == '1003'):
        request.session['price'] = 49.99 * int(request.POST['quantity'])
        request.session['totalorders'] = request.session['totalorders']+int(request.POST['quantity'])
        request.session['totalamount'] = request.session['totalamount'] + request.session['price']
    else:
        print request.session['product_id']
        return redirect('/amadon')
    return redirect('/amadon/checkout')

def checkout(request):
    context = {
        'amount' : request.session['price'],
        'totalorders' : request.session['totalorders'],
        'totalamount' : request.session['totalamount']
    }
    return render(request, "amadon/checkout.html", context)
