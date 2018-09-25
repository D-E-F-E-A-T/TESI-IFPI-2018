from libs.myurllib import get_parsed, session, Moment, easy_get_text

soup = get_parsed('https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi')
#

temperatura_momento = soup.find('p',class_='left normal txt-gray-cw temp-topo').get_text()
condicao_momento = soup.find('p', id='momento-condicao').get_text()
momento_sensacao = soup.find('li', id='momento-sensacao').get_text()
momento_humidade = soup.find('li', id='momento-humidade').get_text()
momento_pressao = soup.find('li', id='momento-pressao').get_text()
momento_vento = soup.find('a', id='momento-vento').get_text().replace(' ','').replace('\n','').replace('\xa0','')
atualizacao = soup.find('p', id='momento-atualizacao').get_text().replace('\n','').replace(' ','').replace('Atualizadoàs','')

#

m = Moment(temperatura_momento, condicao_momento, momento_sensacao, momento_humidade, momento_pressao, momento_vento, atualizacao)

m.save()

# estrutura = {
#     'temperatura_momento':temperatura_momento,
#     'condicao_momento':condicao_momento,
#     'momento_sensacao':momento_sensacao,
#     'momento_humidade':momento_humidade,
#     'momento_pressao':momento_pressao,
#     'momento_vento':momento_vento,
#     'atualizacao':atualizacao
# }

#(estrutura)

#dados = get_data()

#print('                        dados de temperatura                            ')
#print(' horario | temperatura | sensacao | umidade | pressao | vento | condicao')
#print('------------------------------------------------------------------------')

#print(dados)

# for dado in dados:
# 	print(" %s%s| %s%s| %s%s | %s%s | %s%s | %s%s | %s "%(
# 		dado['atualizacao'], (8-len(dado['atualizacao']))*' ',
# 		dado['temperatura_momento'], (12-len(dado['temperatura_momento']))*' ',
# 		dado['momento_sensacao'], (8-len(dado['momento_sensacao']))*' ',
# 		dado['momento_humidade'], (7-len(dado['momento_humidade']))*' ',
# 		dado['momento_pressao'], (7-len(dado['momento_pressao']))*' ',
# 		dado['momento_vento'], (5-len(dado['momento_vento']))*' ',
# 		dado['condicao_momento']))