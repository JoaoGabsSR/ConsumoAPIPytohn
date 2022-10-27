import pymysql.cursors
import requests
import json
from datetime import datetime

'''
http://api.openweathermap.org/data/2.5/weather?q={}&appid={API_KEY}
'''

# Chave de Acesso da API
API_KEY = ''
conexao = pymysql.connect(
	host='localhost',
	user='root',
	password='password',
	database='previsao_de_tempo',
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor
)

if conexao:
	# Cidades
	cidades = ['rio branco', 'maceió', 'macapá', 'manaus', 'salvador', 'fortaleza', 'brasília', 'vitória', 'goiânia', 'são luís',
	          'cuiabá', 'campo grande', 'belo horizonte', 'belém', 'joão pessoa', 'curitiba', 'recife', 'teresinha', 'rio de janeiro',
	          'natal', 'porto alegre', 'porto velho', 'boa vista', 'florianópolis', 'são paulo', 'aracaju', 'palmas']
	temps = [] # Lista para armazenar as temperaturas da requisição
	data_atual = datetime.today() # Data do dia atual
	# print(data_atual)

	# Looping de requisições
	for cidade in cidades:
		url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}'
		request = requests.request('GET', url)
		response = json.loads(request.text)

		temperatura = response['main']['temp']

		temps.append(temperatura)

	# Lista para armazenagem de todas as temperaturas convertidas
	temperaturas_convertidas = {}
	dados = []

	# Looping de conversão das temperaturas
	for cont in range(0, 27):
		k = temps[cont]
		c = k - 273.15
		f = ((k - 273.15) * (9/5) + 32)

		# temperaturas_convertidas.append([f'{cidades[cont]}'], [f'Cº = {c:.1f}'], Fº = {f:.1f}, Kº = {k:.1f}')
		temperaturas_convertidas['cidade'] = cidades[cont].capitalize()
		temperaturas_convertidas['data_atual'] = data_atual.strftime('%d/%m/%Y') + ' ' + data_atual.strftime('%H:%M')
		temperaturas_convertidas['temp_celcius'] = f'{c:.1f}'
		temperaturas_convertidas['temp_kelvin'] = f'{k:.1f}'
		temperaturas_convertidas['temp_fahrenheit'] = f'{f:.1f}'

		dados.append(temperaturas_convertidas.copy())

		temperaturas_convertidas.clear()

	for dado in dados:
		# print(dado)
		# Inserção no banco de dados
		with conexao.cursor() as cursor:
			query = 'INSERT INTO `tb_previsao_de_tempo`(`cidade`, `data_atual`, `temp_celcius`, `temp_kelvin`, `temp_fahrenheit`)' \
			        'VALUES (%s, %s, %s, %s, %s)'
			cursor.execute(query, (dado['cidade'], dado['data_atual'], dado['temp_celcius'],
			                       dado['temp_kelvin'], dado['temp_fahrenheit']))
			conexao.commit() # Salva as mudaças

		print('Inserção no banco de dados realizado com sucesso.')

else:
	print('Erro de Conexão')
