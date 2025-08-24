from django.shortcuts import render, redirect, get_object_or_404
from .models import Tercero, Material
from .forms import TerceroForm, MaterialForm
from django.contrib import messages
import pandas as pd


def menu_maestros(request):
    return render(request, 'maestros/menu_maestros.html')

# Terceros views

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
    query = request.GET.get("q") 
    if query:
        terceros = Tercero.objects.filter(nombre__icontains=query)
    else:
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
    query = request.GET.get("q") 
    if query:
        terceros = Tercero.objects.filter(nombre__icontains=query)
    else:
        terceros = Tercero.objects.all()

    return render(request, "maestros/visualizar_terceros.html", {"terceros": terceros})

############################################################################################
# Materiales views 

# Menú materiales
from .models import Material
def menu_materiales(request):
    return render(request, 'maestros/menu_materiales.html')

# Crear material
def material_crear(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Material creado correctamente")
            return redirect('menu_materiales')
    else:
        form = MaterialForm()
    return render(request, 'maestros/material_form.html', {'form': form, 'titulo': 'Crear Material'})

# Listar materiales
def material_listar(request):
    query = request.GET.get("q") 
    if query:
        materiales = Material.objects.filter(nombre__icontains=query)
    else:
        materiales = Material.objects.all()
    return render(request, 'maestros/material_list.html', {'materiales': materiales})

# Menu para seleccionar qué material editar
def material_editar_menu(request):
    query = request.GET.get("q") 
    if query:
        materiales = Material.objects.filter(nombre__icontains=query)
    else:
        materiales = Material.objects.all()
    return render(request, 'maestros/material_editar_menu.html', {'materiales': materiales})

# Editar material específico
def material_editar(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, "Material actualizado correctamente")
            return redirect('material_listar')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'maestros/material_form.html', {'form': form, 'titulo': 'Editar Material'})

# Carga masiva desde Excel
def material_carga_masiva(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        errores = []

        try:
            df = pd.read_excel(archivo)
            
            # Columnas obligatorias
            columnas_obligatorias = ['nombre', 'tercero']
            for col in columnas_obligatorias:
                if col not in df.columns:
                    errores.append(f"Columna obligatoria '{col}' no encontrada en el Excel.")

            # Validar fila por fila solo si las columnas están presentes
            if not errores:
                for idx, row in df.iterrows():
                    fila_num = idx + 2  # +2 porque pandas indexa desde 0 y la fila 1 es el header
                    fila_errores = []

                    # Nombre y tercero obligatorios
                    if pd.isna(row.get('nombre')):
                        fila_errores.append("Falta 'nombre'")
                    if pd.isna(row.get('tercero')):
                        fila_errores.append("Falta 'tercero'")
                    else:
                        # Verificar que el tercero exista
                        if not Tercero.objects.filter(nombre=row['tercero']).exists():
                            fila_errores.append(f"Tercero '{row['tercero']}' no existe")

                    # Unidad de medida
                    unidad = row.get('unidad_medida', 'un')
                    if unidad not in ['kg', 'lt', 'un', 'cj']:
                        fila_errores.append(f"Unidad de medida '{unidad}' inválida")

                    # Peso bruto >= peso neto
                    peso_neto = row.get('peso_neto')
                    peso_bruto = row.get('peso_bruto')
                    if pd.notna(peso_neto) and pd.notna(peso_bruto):
                        if peso_bruto < peso_neto:
                            fila_errores.append(f"Peso bruto ({peso_bruto}) menor que peso neto ({peso_neto})")
                    
                    # Código de barras único
                    codigo_barras = row.get('codigo_barras')
                    if pd.notna(codigo_barras):
                        if Material.objects.filter(codigo_barras=codigo_barras).exists():
                            fila_errores.append(f"Código de barras '{codigo_barras}' ya existe en la base de datos")
                    # Otros posibles errores opcionales: tipo de dato, duplicados en código de barras
                    # ...

                    if fila_errores:
                        errores.append(f"Fila {fila_num}: " + "; ".join(fila_errores))

            # Si hay errores, mostrar resumen
            if errores:
                return render(request, 'maestros/material_carga_masiva_errores.html', {'errores': errores})

            # Si no hay errores, crear materiales
            for _, row in df.iterrows():
                tercero = Tercero.objects.get(nombre=row['tercero'])
                Material.objects.create(
                    nombre=row['nombre'],
                    descripcion=row.get('descripcion', ''),
                    tercero=tercero,
                    categoria=row.get('categoria'),
                    unidad_medida=row.get('unidad_medida', 'un'),
                    peso_neto=row.get('peso_neto'),
                    peso_bruto=row.get('peso_bruto'),
                    alto=row.get('alto'),
                    ancho=row.get('ancho'),
                    largo=row.get('largo'),
                    condiciones_almacenamiento=row.get('condiciones_almacenamiento'),
                    codigo_barras=row.get('codigo_barras'),
                    valor_declarado=row.get('valor_declarado'),
                    moneda=row.get('moneda', 'ARS'),
                )
            messages.success(request, "Carga masiva realizada correctamente")
            return redirect('menu_materiales')

        except Exception as e:
            errores.append(f"Error al leer el archivo Excel: {e}")
            return render(request, 'maestros/material_carga_masiva_errores.html', {'errores': errores})

    return render(request, 'maestros/material_carga_masiva.html')