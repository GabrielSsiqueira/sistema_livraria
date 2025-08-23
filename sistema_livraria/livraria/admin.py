from django.contrib import admin
from .models import Categoria, Livros, imagemLivros, ImagemCategoria
# Register your models here.

class ImagemLivroInline(admin.TabularInline):
    model = imagemLivros
    extra = 1

class ImagemCategoriaInline(admin.TabularInline):
    model = ImagemCategoria
    extra = 1

@admin.register(Livros)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'preco', 'categoria_id')
    search_fields = ('titulo', 'autor')
    list_filter = ('categoria_id',)
    inlines = [ImagemLivroInline]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao')
    search_fields = ('titulo',)
    inlines = [ImagemCategoriaInline]

admin.site.register(imagemLivros)
