#Classe que representa um modelo de camiseta
class ModeloDeCamiseta:

	#Método construtor da classe
	def __init__(self, cor, tamanho, valor, quantidade):
		self.cor = cor
		self.tamanho = tamanho
		self.valor = valor
		self.quantidade = quantidade

	#Método usado para adicionar uma quantidade de camisetas quando o cadastro do modelo já foi realizado
	def adicionar(self, quantidade):
		self.quantidade += quantidade


#Classe responsável por controlar os modelos cadastrados e vendidos
class Controle:

	#Método construtor da classe
	def __init__(self):
		self.modelosCadastrados = []
		self.modelosVendidos = []

	#Método utilizado para verificar se um modelo ja foi cadastrado
	#Retorno: Modelo já cadastrado -> índice no vetor | Modelo ainda não cadastrado -> -1
	def posicaoDoModeloCadastrado(self, cor, tamanho, valor):
		for i, modelo in enumerate(self.modelosCadastrados):
			if cor == modelo.cor and tamanho == modelo.tamanho and valor == modelo.valor:
				return i
		return -1

	#Método utilizado para verificar se um modelo ja foi cadastrado para venda (Aqui o valor do item tende a ser maior pelo lucro)
	#Retorno: Modelo já cadastrado -> índice no vetor | Modelo ainda não cadastrado -> -1
	def posicaoDoModeloParaVenda(self, cor, tamanho):
		for i, modelo in enumerate(self.modelosCadastrados):
			if cor == modelo.cor and tamanho == modelo.tamanho:
				return i
		return -1

	#Método utilizado para cadastrar um modelo de camiseta.
	#Se o modelo já foi cadastrado, o algoritmo incremente a quantidade do modelo
	def cadastrarModelo(self, cor, tamanho, valor, quantidade):
		posicao = self.posicaoDoModeloCadastrado(cor, tamanho, valor)

		#Tratamento de erros
		if quantidade <= 0:
			print("[ERRO](entrada inválida) - quantidade negativa/nula")
			return

		if posicao == -1:
			novoModeloDeCamiseta = ModeloDeCamiseta(cor, tamanho, valor, quantidade)
			self.modelosCadastrados.append(novoModeloDeCamiseta)
		else:
			self.modelosCadastrados[posicao].adicionar(quantidade)

	#Método utilizado para indicar a venda um modelo de camiseta.
	#Só é possível vender um modelo que foi cadastrado, caso contrário um erro será printado.
	def venderModelo(self, cor, tamanho, valor, quantidade):
		posicao = self.posicaoDoModeloParaVenda(cor, tamanho)

		#Tratamento de erros
		if quantidade <= 0:
			print("[ERRO](entrada inválida) - quantidade negativa/nula")
			return
		if posicao == -1:
			print("erro - tentando vender produto não cadastrado")
			return
		if quantidade > self.modelosCadastrados[posicao].quantidade:
			print("erro - tentando vender mais unidades do que as existentes")
			return

		modeloDeCamisetaVendido = ModeloDeCamiseta(cor, tamanho, valor, quantidade)
		self.modelosVendidos.append(modeloDeCamisetaVendido)

	#Método utilizado para calcular o total de ganho obtido pelas vendas
	#Retorno: Float 
	def calcularGanho(self):
		total = 0
		for modelo in self.modelosVendidos:
			total += modelo.quantidade * modelo.valor
		return total


#Classe responsável por lidar com a geração do relatório. A classe é a única que lida com os arquivos de entrada e saída.
class Relatorio:

	#Método construtor da classe
	def __init__(self):
		self.controle = Controle()

	#Método responsável por gerar o relatório
	#O método é gerencia os arquivos de entrada com permissão de leitura e o de saída com permissão de sobreposição, ou seja, a cada execução o relatório será reescrito.
	def gerar(self, nomeDoArquivo):
		entrada = open(nomeDoArquivo, 'r')
		saida = open('relatorio.txt', 'w')

		for linha in entrada:

			#Tratamento da linha e separação em um vetor
			info = linha.replace('\n', '').replace(',', '.').split()

			operador = info[0]

			#Comando responsável por identificar o fim do arquivo
			if operador == '!':
				return

			#Comando responsável por exibir os modelos cadastrados em ordem
			if operador == '/':
				for modelo in self.controle.modelosCadastrados:
					saida.write(str(modelo.cor) + ' ' + str(modelo.tamanho) + ' ' + str(modelo.quantidade) + ' ' + str(modelo.valor) + ' ' + '\n')
				saida.write('0\n')

			#Comando responsável por exibir os modelos vendidos em ordem
			if operador == '\\':
				for modelo in self.controle.modelosVendidos:
					saida.write(str(modelo.cor) + ' ' + str(modelo.tamanho) + ' ' + str(modelo.quantidade) + ' ' + str(modelo.valor) + ' ' + '\n')
				saida.write('0\n')

			#Comando responsável por exibir o total de ganho das vendas
			if operador == '*':
				saida.write(str(self.controle.calcularGanho()) + '\n')
				saida.write('0\n')

			#Comando responsável identificar o cadastrar um modelo
			if operador == '+':
				cor = info[1]
				tamanho = info[2]
				quantidade = int(info[3])
				valor = float(info[4])

				self.controle.cadastrarModelo(cor, tamanho, valor, quantidade)
				saida.write('0\n')

			#Comando responsável identificar uma venda de modelo
			if operador == '-':
				cor = info[1]
				tamanho = info[2]
				quantidade = int(info[3])
				valor = float(info[4])

				self.controle.venderModelo(cor, tamanho, valor, quantidade)
				saida.write('0\n')

		entrada.close()
		saida.close()


#Geração do relatório
relatorio = Relatorio()
relatorio.gerar("dados.txt")
