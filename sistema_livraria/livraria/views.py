from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required 
from django.conf import settings
from .forms import LivroForm, CategoriaForm, ContatoForm
from .models import Categoria, Livros, imagemLivros, ImagemCategoria, Contato
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

def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com Sucesso')
            return redirect('contato')
    
    else:
        form = ContatoForm()
    return render(request, 'contato.html', {'form': form})

def adicionar_carrinho(request, pk):
    livro = get_object_or_404(Livros, pk=pk)
    imagem = imagemLivros.objects.filter(livro_id=pk).first()

    url_imagem = f"{settings.MEDIA_URL}livros/{imagem.img_base64}" if imagem else None

    carrinho = request.session.get("carrinho", {})

    if str(pk) in carrinho:
        if carrinho[str(pk)]["quantidade"] < livro.quantidade_estoque:
            carrinho[str(pk)]["quantidade"] += 1
    else:
        if livro.quantidade_estoque > 0: 
            carrinho[str(pk)] = {
                "titulo" : livro.titulo,
                "descricao": livro.descricao,
                "preco": float(livro.preco),
                "quantidade": 1, 
                "imagem": url_imagem
            }
    
    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect('ver_carrinho')
    
def ver_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    total = sum(item["preco"] * item["quantidade"] for item in carrinho.values())

    return render(request, "carrinho.html", {"carrinho": carrinho, "total": total})

def atualizar_carrinho(request, pk, acao):
    livro = get_object_or_404(Livros, pk=pk)

    carrinho = request.session.get("carrinho", {})

    if str(pk) in carrinho:
        if acao == "mais":
           if carrinho[str(pk)]["quantidade"] < livro.quantidade_estoque:
            carrinho[str(pk)]["quantidade"] += 1
            
        elif acao == "menos":
            carrinho[str(pk)]["quantidade"] -= 1
            if carrinho[str(pk)]["quantidade"] <= 0:
                del carrinho[str(pk)]
    
    request.session["carrinho"] = carrinho
    request.session.modified = True

    return redirect("ver_carrinho")

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

def listar_contato(request):
    contatos = Contato.objects.all()
    return render(request, 'admin/listar_contato.html', { 'contatos': contatos })

def excluir_contato(request, pk):
    contato = get_object_or_404(Contato, pk=pk)

    if request.method == 'POST':
        contato.delete()
        return redirect('listar_contato')
    
    return render(request, 'admin/excluir_contato.html', {'contato': contato})

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

