from django.shortcuts import render, redirect, get_object_or_404
from .models import Tercero
from .forms import TerceroForm

def menu_maestros(request):
    return render(request, 'maestros/menu_maestros.html')


def menu_terceros(request):
    return render(request, 'maestros/menu_terceros.html')

def crear_tercero(request):
    if request.method == 'POST':
        form = TerceroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_terceros')
    else:
        form = TerceroForm()
    return render(request, 'maestros/crear_tercero.html', {'form': form})

def modificar_tercero(request):
    terceros = Tercero.objects.all()
    return render(request, 'maestros/modificar_tercero.html', {'terceros': terceros})

def editar_tercero(request, pk):
    tercero = get_object_or_404(Tercero, pk=pk)
    if request.method == 'POST':
        form = TerceroForm(request.POST, instance=tercero)
        if form.is_valid():
            form.save()
            return redirect('modificar_tercero')
    else:
        form = TerceroForm(instance=tercero)
    return render(request, 'maestros/editar_tercero.html', {'form': form, 'tercero': tercero})

def visualizar_terceros(request):
    terceros = Tercero.objects.all()
    return render(request, 'maestros/visualizar_terceros.html', {'terceros': terceros})
