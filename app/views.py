from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import sys
import logging

from utils import helper
from .dominio import *
from .dao import DAOFactory
from .services import CategoriaService, ProdutoService


def home(request):
    """Exibe a página inicial da aplicação"""
    template = 'home.html'
    return render(request, template)


def categorias(request, acao=None, id=None):
    """Gerencia as operações CRUD para categorias usando Services"""
    try:
        service = CategoriaService()

        # listar registros 
        if acao is None:
            registros = service.listar_todas()
            return render(request, 'categorias_listar.html', context={'registros': registros})
        
        # salvar registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            if acao_form == 'Inclusão':
                try:
                    service.criar_categoria(form_data['descricao'])
                    messages.success(request, 'Categoria incluída com sucesso!')
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, 'categorias_editar.html', {
                        'acao': 'Inclusão',
                        'obj': {'descricao': form_data['descricao']}
                    })

            elif acao_form == 'Exclusão':
                try:
                    service.excluir_categoria(int(form_data['id']))
                    messages.success(request, 'Categoria excluída com sucesso!')
                except ValueError as e:
                    messages.error(request, str(e))

            else:  # Alteração
                try:
                    service.atualizar_categoria(int(form_data['id']), form_data['descricao'])
                    messages.success(request, 'Categoria alterada com sucesso!')
                except ValueError as e:
                    messages.error(request, str(e))
                    obj = service.obter_por_id(int(form_data['id']))
                    return render(request, 'categorias_editar.html', {
                        'acao': 'Alteração',
                        'obj': obj
                    })

            return HttpResponseRedirect(reverse("categorias"))
        
        # inserir registro
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html', {'acao': 'Inclusão'})
        
        # alterar ou excluir
        elif acao in ['alterar', 'excluir']:
            acao_display = 'Alteração' if acao == 'alterar' else 'Exclusão'
            obj = service.obter_por_id(int(id))
            if not obj:
                messages.error(request, 'Categoria não encontrada.')
                return HttpResponseRedirect(reverse("categorias"))
            return render(request, 'categorias_editar.html', {'acao': acao_display, 'obj': obj})
        
        else:
            raise Exception('Ação inválida')

    except Exception as err:
        logging.error(f"Erro em categorias: {err}")
        messages.error(request, f'Erro: {err}')
        return render(request, 'home.html', context={'ERRO': err})
        
        # inserir registro
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html', {'acao': 'Inclusão'})
        
        # alterar ou excluir
        elif acao in ['alterar', 'excluir']:
            acao = 'Alteração' if acao == 'alterar' else 'Exclusão'
            # seleciona o registro pelo id informado
            obj = dao.selecionar_um(id)
            return render(request, 'categorias_editar.html', {'acao': acao, 'obj': obj})
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


def produtos(request, acao=None, id=None):
    """Gerencia as operações CRUD para produtos usando Services"""
    try:
        produto_service = ProdutoService()
        categoria_service = CategoriaService()

        # listar registros 
        if acao is None:
            registros = produto_service.listar_todos()
            return render(request, 'produtos_listar.html', context={'registros': registros})
        
        # salvar registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            if acao_form == 'Inclusão':
                try:
                    produto_service.criar_produto(
                        descricao=form_data['descricao'],
                        preco_unitario=float(form_data['preco_unitario']),
                        quantidade_estoque=int(form_data['quantidade_estoque']) if form_data['quantidade_estoque'] else 0,
                        categoria_id=int(form_data['categoria_id'])
                    )
                    messages.success(request, 'Produto incluído com sucesso!')
                except (ValueError, TypeError) as e:
                    messages.error(request, str(e))
                    categorias = categoria_service.listar_todas()
                    return render(request, 'produtos_editar.html', {
                        'acao': 'Inclusão',
                        'categorias': categorias,
                        'obj': {
                            'descricao': form_data['descricao'],
                            'preco_unitario': form_data['preco_unitario'],
                            'quantidade_estoque': form_data['quantidade_estoque'],
                            'categoria_id': form_data['categoria_id']
                        }
                    })

            elif acao_form == 'Exclusão':
                try:
                    produto_service.excluir_produto(int(form_data['id']))
                    messages.success(request, 'Produto excluído com sucesso!')
                except ValueError as e:
                    messages.error(request, str(e))
            
            else:  # Alteração
                try:
                    produto_service.atualizar_produto(
                        id=int(form_data['id']),
                        descricao=form_data['descricao'],
                        preco_unitario=float(form_data['preco_unitario']),
                        quantidade_estoque=int(form_data['quantidade_estoque']) if form_data['quantidade_estoque'] else 0,
                        categoria_id=int(form_data['categoria_id'])
                    )
                    messages.success(request, 'Produto alterado com sucesso!')
                except (ValueError, TypeError) as e:
                    messages.error(request, str(e))
                    obj = produto_service.obter_por_id(int(form_data['id']))
                    categorias = categoria_service.listar_todas()
                    return render(request, 'produtos_editar.html', {
                        'acao': 'Alteração',
                        'obj': obj,
                        'categorias': categorias
                    })

            return HttpResponseRedirect(reverse("produtos"))
        
        # inserir registro
        elif acao == 'incluir':
            categorias = categoria_service.listar_todas()
            return render(request, 'produtos_editar.html', {
                'acao': 'Inclusão', 
                'categorias': categorias
            })
        
        # alterar ou excluir
        elif acao in ['alterar', 'excluir']:
            produto = produto_service.obter_por_id(int(id))
            if not produto:
                messages.error(request, 'Produto não encontrado.')
                return HttpResponseRedirect(reverse("produtos"))
            
            categorias = categoria_service.listar_todas()
            acao_display = 'Alteração' if acao == 'alterar' else 'Exclusão'

            return render(request, 'produtos_editar.html', {
                'acao': acao_display, 
                'obj': produto, 
                'categorias': categorias
            })
        
        else:
            raise Exception('Ação inválida')

    except Exception as err:
        logging.error(f"Erro em produtos: {err}")
        messages.error(request, f'Erro: {err}')
        return render(request, 'home.html', context={'ERRO': err})


def obter_categorias():
    """Função auxiliar para obter todas as categorias (compatibilidade)"""
    service = CategoriaService()
    return service.listar_todas()




