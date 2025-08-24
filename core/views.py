from django.shortcuts import render

def menu_principal(request):
    return render(request, 'core/menu_principal.html')
