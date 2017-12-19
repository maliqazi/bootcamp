from django.shortcuts import render, HttpResponse, redirect

def index(request):
    context = {
        'somekey' : 'somevalue'
    }
    return render(request, "survey_app/index.html", context)

def process(request):
    counter=request.session.get('counter', 0)
    request.session['counter'] = counter+1
    request.session['name'] = request.POST['name']
    request.session['location'] = request.POST['location']
    request.session['language'] = request.POST['language']
    request.session['desc'] = request.POST['desc']
    return redirect('/result')

def result(request):
    context = {
        'name' : request.session['name'],
        'location' : request.session['location'],
        'language' : request.session['language'],
        'desc' : request.session['desc'],
        'counter' : request.session['counter']
    }
    return render(request, "survey_app/result.html", context)
