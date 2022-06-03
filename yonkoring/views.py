from django.shortcuts import render

def error_handle(request, exception):
    return render(request, 'error_page.html')

def error_handle_500(request):
    return render(request, 'error_page.html')