from django.db import models

# Create your models here.

class Categoria (models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class ImagemCategoria(models.Model):
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='imagens_categorias')
    img_base64 = models.TextField()

    def __str__(self):
        return f"Imagem da Categoria:{self.categoria.titulo}"

class Livros (models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    autor = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='livros')

    def __str__(self):
        return self.titulo

class imagemLivros(models.Model):
    livro_id = models.ForeignKey(Livros, on_delete=models.CASCADE, related_name='imagens')
    img_base64 = models.TextField()

    def __str__(self):
        return f"Imagem do Livro: {self.livros.titulo}"
