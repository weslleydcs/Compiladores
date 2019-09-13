#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import string

erro = False
buffer = []
permitidos = ['=', '+', '-', '/', '*', '^', '%', '>', '<', '[', ']', '{', '}', '(', ')', ',', ';']

for e in sys.stdin.read():
	buffer.append(e)


for caractere in buffer:
	if ( (ord(caractere) < 32 or ord(caractere) > 126) and (ord(caractere) != 9 and ord(caractere) != 10) ):
		erro = True
		break

if erro:
	print "ARQUIVO INVALIDO"
	sys.exit()

#------------------------------------------------------------------------------------------------------------------------------------------Função Principal------------------------------------------------------------------------------------------------------------------------------------------

#Função de aspas duplas
def AspasDuplas(indice, linha, coluna):
	
	linha_aux = 0
	coluna_aux = 0
	
	if (indice == len(buffer) - 1): 
		return False, indice, linha, coluna, False
		
	indice += 1 #já li 1, posso ler + 128
	coluna += 1
	
	contador_aspas = 1
	Ultimo_eh_barra_n = False
	Encontrei = False
	Final_Arquivo = False
	
	while (contador_aspas != 130): # 
		
		if (buffer[indice] == '"'):
			Encontrei = True
			break
		
		if (indice == len(buffer) - 1): 
			Final_Arquivo = True
			break
		
		if (buffer[indice] == '\n' and contador_aspas == 129): #um barra n na última posição
			indice += 1
			coluna += 1
			break 
		
		if (buffer[indice] == '\n' and contador_aspas != 128):
			linha += 1
			coluna = 0
			
		if (buffer[indice] == '\n' and contador_aspas == 128):
			Ultimo_eh_barra_n = True
			linha_aux = linha
			coluna_aux = coluna
			linha += 1
			coluna = 0
			
		contador_aspas += 1
		indice += 1
		coluna += 1
			
	if (Encontrei == False and Final_Arquivo == True): #caso em que o arquivo acabou e não encontrou uma aspas
		return False, indice , linha, coluna, False
			
	if (Encontrei == False and Ultimo_eh_barra_n == False): #caso em que não encontra uma " para fechar
		return False, indice - 2, linha, coluna - 2, False
		
	if (Encontrei == False and Ultimo_eh_barra_n == True): #caso em que o último caractere é um \n e não acha
		#print "caso 3"
		return False, indice - 2, linha_aux, coluna_aux, True #Este True é só neste caso
		
	if (Encontrei == True): #caso em que encontra uma "
		return True, indice, linha, coluna, False


#Função de aspas simples
def AspasSimples(indice, linha, coluna):
	
	if (indice == len(buffer) - 1):
		return False, indice, linha, coluna
		
	indice += 1
	coluna += 1
		
	if (buffer[indice] == "'"): #caso '' ---> 1 1, 1 2 .... da erro no anterior porque já leu uma aspas, incrementa a coluna e o indice da erro dnv pq dps é eof
		return False, indice - 1, linha, coluna - 1 #verificar o return do indice

	if (buffer[indice] != "'" and indice == len(buffer) - 1): #caso 'a #erro dps do a que é eof
		return False, indice - 1, linha, coluna #acho que coluna - 1 também

	if (buffer[indice] == '\n' and buffer[indice + 1] != "'"): #caso '\nW
		return False, indice - 1, linha, coluna

	if (buffer[indice] != '\n' and buffer[indice] != "'" and buffer[indice + 1] != "'"): #caso 'ab
		return False, indice, linha, coluna 

	if (buffer[indice] == '\n' and buffer[indice + 1] == "'"): #caso '\n'
		linha += 1
		coluna = 1
		return True, indice + 1, linha, coluna #return True, indice + 1, linha, coluna

	if (buffer[indice] != "'" and buffer[indice + 1] == "'"): #caso 'a'
		return True, indice + 1, linha, coluna + 1

	
#Função de letras	
def le_char(indice, linha, coluna): 

	if (buffer[indice].isalpha() or buffer[indice] == '_'): #lê letra ou _
		return True, indice, linha, coluna
	
	if (buffer[indice].isdigit()): #lê numero
		return True, indice, linha, coluna
		
	if (buffer[indice] in permitidos): #lê algum operador 
		contador_letra = 0
		return True, indice, linha, coluna 	
		
	if (buffer[indice] == '.'): #lê um ponto, dá erro numa casa antes
		return False, indice, linha, coluna	
		
	if (buffer[indice] != '!' and buffer[indice] not in permitidos): #se não for uma ! e não estiver em simbolos permitidos lê simbolo nao permitido, dá erro nessa casa
		return False, indice, linha, coluna	
		
	if (indice == len(buffer) - 1):	#se for a última posição e for um !
		return False, indice, linha, coluna
		
	if (buffer[indice + 1] == '='): #não é a última posição como visto acima, no último if, então posso olhar a próxima
		contador_letra = 0
		return True, indice + 1, linha, coluna + 1
		
	if (buffer[indice + 1] != '='): #tem que dar erro nela pois não achou um =
		return False, indice, linha, coluna	
	
#Função de inteiros
def le_inteiro(indice, linha, coluna): #o último retorno True é se for um real
	
	if (buffer[indice].isdigit()): #lê numero
		return True, indice, linha, coluna, False
		
	if (buffer[indice] in permitidos): #lê algum operador ##################################REVER##################################
		contador_inteiro = 0
		return True, indice, linha, coluna, False	
		
	if (buffer[indice] == '.'): #lê '.' e vira um real
		return True, indice, linha, coluna, True	
	
	if (buffer[indice].isalpha() or buffer[indice] == '_'): #lê letra ou _, dá erro uma casa antes
		return False, indice - 1, linha, coluna - 1, False
		
	if (buffer[indice] != '!' and buffer[indice] not in permitidos): #lê simbolo nao permitido, dá erro nessa casa
		return False, indice, linha, coluna, False
		
	if (indice == len(buffer) - 1):	#se for a última posição e for um !
		return False, indice, linha, coluna, False
		
	if (buffer[indice + 1] == '='): #não é a última posição como visto acima, no último if, então posso olhar a próxima
		contador_inteiro = 0
		return True, indice + 1, linha, coluna + 1, False
		
	if (buffer[indice + 1] != '='): #tem que dar erro nela pois não achou um =
		return False, indice, linha, coluna, False
	
	
#Função de reais
def le_real(indice, linha, coluna): # o último retorno do True é apenas para tratamento de 7..

	if (buffer[indice].isdigit()): #lê numero
		return True, indice, linha, coluna, False
		
	if (buffer[indice] in permitidos): #lê algum operador ##################################REVER##################################
		contador_real = 0
		contador_inteiro = 0
		return True, indice, linha, coluna, False	
		
	if (buffer[indice] == '.' and Real_ponto == False): #lê um ponto, é de boa
		return True, indice, linha, coluna, True		
		
	if (buffer[indice] == '.' and Real_ponto == True): #lê outro . ...dá erro uma casa antes
		return False, indice - 1, linha, coluna - 1, True	
	
	if (buffer[indice].isalpha() or buffer[indice] == '_'): #lê letra ou _, dá erro uma casa antes
		return False, indice - 1, linha, coluna - 1, False
		
	if (buffer[indice] != '!' and buffer[indice] not in permitidos): #lê simbolo nao permitido, dá erro nessa casa
		return False, indice, linha, coluna, False
		
	if (indice == len(buffer) - 1):	#se for a última posição e for um !
		return False, indice, linha, coluna, False
		
	if (buffer[indice + 1] == '='): #não é a última posição como visto acima, no último if, então posso olhar a próxima
		contador_real = 0
		contador_inteiro = 0
		return True, indice + 1, linha, coluna + 1, False
		
	if (buffer[indice + 1] != '='): #tem que dar erro nela pois não achou um =
		return False, indice, linha, coluna, False
			
	
def retornaTipoToken(elemento):

	if (elemento == '\n'): #Quebra linha
		return "quebraLinha"
		
	if (elemento == '"'):
		return "AspasDuplas"
		
	if (elemento == "'"):
		return "AspasSimples"
		
	if (elemento in permitidos or elemento == chr(9) or elemento == chr(10) or elemento == chr(32)):
		return "controle"	
		
	if ((elemento.isalpha() or elemento == '_') and Estado_Inteiro == False and Estado_Real == False): #Lê letras ou _ no estado letra
		return "letra"
		
	if (elemento.isdigit() and Estado_Letra == True): #Lê inteiros no estado letra
		return "letra"
		
	if (elemento == '.' and Estado_Letra == True): #Vai dar erro a ser tratado na função de letras
		return "letra"	
	
	if (elemento.isdigit() and Estado_Letra == False): #Posso ler inteiros
		return "inteiro"
	
	if ((elemento.isalpha() or elemento == '_') and Estado_Inteiro == True): #Vai dar erro a ser tratado na função de inteiros
		return "inteiro"
	
	if (elemento == '.' and Estado_Inteiro == True): #Muda para estado real
		return "real"
		
	if (elemento == '.' and Estado_Real == True): #É pra dar erro lá no tratamento de real lendo o segundo ponto
		return "real"
		
	if ((elemento.isalpha() or elemento == '_') and Estado_Inteiro == False and Estado_Real == True): #Lê letras ou _ no estado real
		return "real"	
		
	if (elemento == '.'): #É pra dar erro de simbolo nao permitido
		return "nao_permitidos"	
		
	if (elemento == '!' and Estado_Letra == True): #É pra tratar lá em letra
		return "letra"	
		
	if (elemento == '!' and Estado_Inteiro == True): #É pra tratar lá em inteiro
		return "inteiro"
		
	if (elemento == '!' and Estado_Real == True): #É pra tratar lá em real
		return "real"	
		
	if (elemento is '!'): #Não está em nenhum estado e é exclamação
		return "exclamacao"	
		
	if (elemento not in permitidos and elemento is not '!'): #É pra dar erro de simbolo nao permitido porque não é nem . nem !
		return "nao_permitidos"	
	

#Variáveis principais
linha = 1
coluna = 0
indice = 0

#Variável responsável por ativar print de erro
qtd_erros = 0

#Variáveis de Contadores
contador_letra = 0
contador_inteiro = 0
contador_real = 0

#Booleanos para tratamento de aspas duplas
Erro_Aspas_Duplas = False
Ultimo_eh_barra_n = False

#Booleanos para tratamento de aspas simples
Erro_Aspas_Simples = False

#Booleanos para tratamento de letras
Estado_Letra = False
Erro_letra = False

#Booleanos para tratamento inteiros
Estado_Inteiro = False
Erro_inteiro = False
Reseta_inteiro = False #rever se precisa
Muda_int_Real = False

#Booleanos para tratamento de real
Estado_Real = False
Erro_real = False
Real_ponto = False


while (indice < len(buffer)):
	
	coluna += 1
	token = retornaTipoToken(buffer[indice])
	
	#print "DEBUG", linha, coluna, ord(buffer[indice]), token, contador_letra
	
	if (token is "quebraLinha"):
		linha += 1
		coluna = 0
		token = "controle" 
		
	if (token is "exclamacao"):

		if (indice == len(buffer) - 1):
			token = "nao_permitidos"
		else:
			if (buffer[indice + 1] == '='):
				#caractere += 1
				#coluna += 1
				token = "controle"
			else:
				token = "nao_permitidos"	
		
	
	if (token is "AspasDuplas"):
		
		Erro_Aspas_Duplas, indice, linha, coluna, Ultimo_eh_barra_n = AspasDuplas(indice, linha, coluna) #, eh_barra_n
		
		if (Erro_Aspas_Duplas == False):
			qtd_erros += 1
			print linha, coluna
			
		if (Ultimo_eh_barra_n == True): #ACHO QUE NÃO PRECISA DAQUI PQ EU INCREMENTO LINHA E COLUNA... DPS na próxima chamada do índice leio outra quebra de linha e faço novamente
			linha += 1
			coluna = 0
			
		token = "controle"

	if (token is "AspasSimples"):
		
		Erro_Aspas_Simples, indice, linha, coluna = AspasSimples(indice, linha, coluna)
	
		if (Erro_Aspas_Simples == False):
			qtd_erros += 1
			print linha, coluna	
			
		token = "controle"
	
	if (token is "letra"):
	
		Estado_Letra = True
		contador_letra += 1

		if (contador_letra == 257):
			qtd_erros += 1
			coluna -= 1
			indice -= 1
			print linha, coluna
			token = "controle"
			
		else:
			Erro_letra, indice, linha, coluna = le_char(indice, linha, coluna)

			if (buffer[indice] == '='):
				token = "controle"

			if (Erro_letra == False):
				qtd_erros += 1
				print linha, coluna
				token = "controle"
				
	if (token is "inteiro"):
		
		Estado_Inteiro = True
		contador_inteiro += 1

		if (contador_inteiro == 65):
			qtd_erros += 1
			coluna -= 1
			indice -= 1
			print linha, coluna
			token = "controle"

		else:
			Erro_inteiro, indice, linha, coluna, Muda_int_Real = le_inteiro(indice, linha, coluna)

			if (buffer[indice] == '='):
				token = "controle"

			if (Erro_inteiro == False):
				qtd_erros += 1
				print linha, coluna
				token = "controle"
				
			if (Muda_int_Real == True): #print "MUDA ESTADO", Estado_Inteiro ACHO QUE NÃO ESTÁ CAINDO AQUI E VER TB NA FUNÇÃO DE REAL SE PRECISA DO if (buffer[indice] == '.'):
				contador_inteiro = 0
				Estado_Inteiro = False
				Estado_Real = True
	
	if (token is "real"):

		Estado_Inteiro = False
		Estado_Real = True #acho que não precisa visto que no tratamento do inteiro eu mudo pra real
		contador_inteiro += 1 #contador_inteiro

		if (contador_inteiro == 65): #contador_inteiro
			qtd_erros += 1
			coluna -= 1
			indice -= 1
			print linha, coluna
			token = "controle"
			
		else:
			Erro_real, indice, linha, coluna, Real_ponto = le_real(indice, linha, coluna)

			if (buffer[indice] == '='):
				token = "controle"

			if (Erro_real == False):
				qtd_erros += 1
				print linha, coluna
				token = "controle"
				
			if (Erro_real == False and Real_ponto == True): #se tiver erro e se ler mais um ponto
				Real_ponto = False
	
	
	if (token is "nao_permitidos"):
		qtd_erros += 1
		print linha, coluna
		token = "controle"
	
	if (token is "controle"):
		
		Estado_Letra = False
		Estado_Inteiro = False
		Estado_Real = False
		Real_ponto = False
		contador_letra = 0
		contador_inteiro = 0
		contador_real = 0
		
	indice += 1	

if (qtd_erros == 0):
	print "OK"