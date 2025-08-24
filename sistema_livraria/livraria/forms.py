from django import forms
from .models import Livros, imagemLivros, Categoria, ImagemCategoria, Contato

class LivroForm(forms.ModelForm):
    imagem = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control' }))
    class Meta:
        model = Livros
        fields = ['titulo', 'descricao', 'autor', 'preco', 'quantidade_estoque',  'categoria_id', 'imagem']
        widget = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria_id': forms.Select(attrs={'class': 'form-control'}),
        }
    

class CategoriaForm(forms.ModelForm):
    imagem = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control' }))

    class Meta:
        model = Categoria
        fields = ['titulo', 'descricao']
        widget = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        widget = {
            'nome' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu E-mail'}),
            'mensagem' : forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Mensagem'}),
        }
