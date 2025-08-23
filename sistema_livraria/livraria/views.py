from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required 
from django.conf import settings
from .forms import LivroForm, CategoriaForm
from .models import Categoria, Livros, imagemLivros, ImagemCategoria
import base64
import os 
import uuid

# Create your views here.

def index(request):
    categorias = Categoria.objects.all()
    return render(request, 'index.html', {'categorias': categorias, 'MEDIA_URL': settings.MEDIA_URL})

def livros(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    livros = Livros.objects.filter(categoria_id=categoria)
    return render(request, 'livros.html', {'categoria': categoria, 'livros': livros, 'MEDIA_URL': settings.MEDIA_URL })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        user = authenticate(request, username=nome , password=senha)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'usuario ou senha inválidos')
    return render(request, 'admin/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@staff_member_required
def dashboard(request):
    return render(request, 'admin/painel.html')


def listar_livros(request):
    livros = Livros.objects.all()
    return render(request, 'admin/listar_livros.html', {'livros': livros })

def cadastrar_livros(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livros = form.save()

            imagens = request.FILES.getlist('imagem')

            pasta_destino = os.path.join(settings.MEDIA_ROOT, 'livros')
            os.makedirs(pasta_destino, exist_ok=True)

            for img in imagens:
                nome_arquivo = f"{uuid.uuid4().hex}{img.name}" # nome unico

                caminho_completo = os.path.join(pasta_destino, nome_arquivo)

                with open(caminho_completo, 'wb+') as destino:
                    for chunk in img.chunks():
                        destino.write(chunk)

                imagemLivros.objects.create(livro_id=livros, img_base64=nome_arquivo)
            
            return redirect('listar_livros')
    
    else:
        form = LivroForm()
    return render(request, 'admin/cadastrar_livros.html', { 'form': form })

def editar_livro(request, pk):
    livro = get_object_or_404(Livros, pk=pk)

    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES, instance=livro)

        if form.is_valid():
            form.save()
            return redirect('listar_livros')

    else:
        form = LivroForm(instance=livro)
    return render(request, 'admin/editar_livro.html', {'form': form, 'livro': livro })

def excluir_livro(request, pk):
    livro = get_object_or_404(Livros, pk=pk)
    
    if request.method == 'POST':
        livro.delete()
        return redirect('listar_livros')
    
    return render(request, 'admin/excluir_livro.html', {'livro': livro})

def listar_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'admin/listar_categoria.html', { 'categorias': categorias })

def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            categorias = form.save()

            imagens = request.FILES.getlist('imagem')

            pasta_destino = os.path.join(settings.MEDIA_ROOT, 'categoria')
            os.makedirs(pasta_destino, exist_ok=True)

            for img in imagens:
                nome_arquivo = f"{uuid.uuid4().hex}{img.name}" #nome unico

                caminho_completo = os.path.join(pasta_destino, nome_arquivo)

                with open(caminho_completo, 'wb+') as destino:
                    
                    for chunk in img.chunks():
                        destino.write(chunk)

                ImagemCategoria.objects.create(categoria_id=categorias, img_base64=nome_arquivo)
            
            return redirect('listar_categoria')

    else:
        form = CategoriaForm()
    return render(request, 'admin/cadastrar_categoria.html', {'form': form})


def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)

        if form.is_valid():
            form.save()
            return redirect('listar_categoria')

    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'admin/editar_categoria.html', {'form': form, 'categoria': categoria })


def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categoria')
    
    return render(request, 'admin/excluir_categoria.html', {'categoria': categoria})

