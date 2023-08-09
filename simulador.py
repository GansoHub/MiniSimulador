#Crie e exclua arquivos e diretórios;
#Realize a listagem de arquivos de um diretório;
#A cada operação realizada pelo usuário, a alocação deve ser simulada (não apenas mostrar a interface para o 
#usuário, mas também como ficaria em baixo nível - alocação no SA - por exemplo, mostrando em que bloco cada 
#arquivo e diretório se encontra);
#As informações dos arquivos e diretórios devem conter, pelo menos, nome e tamanho
#Para facilitar, não permitir arquivos e diretórios com nomes iguais e não precisa implementar várias 
#hierarquias de árvore de diretórios (bastaria dois níveis - um para a raiz e outro para alocar arquivos 
#em um diretório criado).
#Estabelecer o tamanho máximo de memória física (em qualquer unidade, MB, KB, etc.) e tamanho dos blocos 
#(na mesma unidade da memória física, para facilitar);
#Indicar se há fragmentação interna ou externa (quando ocorrer).

import os
arquivo = 0

class arquivo:
    def __init__(self, nome, tamanho):
        self.nome = nome
        self.tamanho = tamanho
        self.proxima_aloca = None

class diretorio:
    def __init__(self, nome):
        self.nome = nome
        self.arquivos = []


def criararquivo(arquivo):
 nome = str(input("digite o nome do arquivo: "))
 tamanho = str(input("digite o tamanho do arquivo: "))
 print (arquivo)

 def bloco(bloco):
    arquivo = this.arquivo

