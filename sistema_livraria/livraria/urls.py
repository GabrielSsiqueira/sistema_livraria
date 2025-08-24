from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index, name='index'),
    path('categoria/<int:categoria_id>/', views.livros, name='livros'),
    path('contato/', views.contato, name='contato'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:pk>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/atualizar/<int:pk>/<str:acao>/', views.atualizar_carrinho, name='atualizar_carrinho'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.dashboard, name='dashboard'),
    path('admin-panel/listar_livros', views.listar_livros, name='listar_livros'),
    path('admin-panel/cadastrar_livro', views.cadastrar_livros, name='cadastrar_livros'),
    path('admin-panel/<int:pk>/editar_livro', views.editar_livro, name='editar_livro'),
    path('admin-panel/<int:pk>/excluir_livro', views.excluir_livro, name='excluir_livro'),
    path('admin-panel/listar_categoria', views.listar_categoria, name='listar_categoria'),
    path('admin-panel/cadastrar_categoria', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('admin-panel/<int:pk>/editar_categoria', views.editar_categoria, name='editar_categoria'),
    path('admin-panel/<int:pk>/excluir_categoria', views.excluir_categoria, name='excluir_categoria'),
    path('admin-panel/listar_contato', views.listar_contato, name='listar_contato'),
    path('admin-panel/<int:pk>/excluir_contato', views.excluir_contato, name='excluir_contato')
]