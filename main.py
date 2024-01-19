import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

TOKEN = "6578313094:AAENzuhD6o9du-uaYE3UWtCTxdC-FZKgutk"
URL = "web-gpt-3-py-madeinna8977"
MSG_RETURN = "WEBHOOK SALVO POR @KiritoModder!!"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Lista de IDs de usuarios e gp premium
premium_users = [5762483448, 6559100564]

allowed_group_ids = [-1001935823289,-1001975508241]

def is_user_allowed(user_id, chat_id):
    return user_id in premium_users or chat_id in allowed_group_ids

def get_user_name(message):
    return message.from_user.first_name if message.from_user.first_name else "Usuario"

def start(message):
    user_name = get_user_name(message)
    welcome_message = (
        f"🤖 Olá {user_name}!\n"
        "Sou o SistenRobot, sou um bot de consultas meus planos estão abaixo.\n\n"
        "Menu de Planos:\n"
        "7 dias por 5.00\n"
        "15 dias por 12.00\n"
        "30 dias por 20.00\n\n"
        "Para adquirir seu plano entre em contato com @Webzin116\n"
        "Certifique que o nome da conta para transação é Lucas Pereira\n"
        "Se estiver com alguma duvida chame o suporte\n"
        "Aproveite que somos o serviço mais barato "
    )
    bot.send_message(message.chat.id, welcome_message, reply_markup=buttons)

@app.route(f'/{TOKEN}', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://{URL}.replit.app/{TOKEN}')
    return MSG_RETURN

def handle_messages(message):
    if message.text == '/start':
        start(message)
    elif message.text == '/menu':
        show_menu(message)
    # Verifica se o usuÃ¡rio Ã© premium ou se estÃ¡ no grupo permitido antes de executar outros comandos
    elif is_user_allowed(message.from_user.id, message.chat.id):
        # Coloque aqui a lÃ³gica para os comandos permitidos para usuÃ¡rios premium ou em grupos permitidos
        if message.text.startswith('/tel1') or message.text.startswith('/tel1'):
            handle_tel1(message)
        elif message.text.startswith('/tel2'):
            handle_tel2(message)
        elif message.text.startswith('/cpf2'):
            handle_cpf2(message)
        elif message.text.startswith('/cpf1'):
            handle_cpf1(message)
        elif message.text.startswith('/placa'):
            handle_placa(message)
        elif message.text.startswith('/nome'):
            handle_nome(message)
        elif message.text.startswith('/cnpj1'):
            handle_cnpj1(message)
        elif message.text.startswith('/cep') or message.text.startswith('/cep'):
            handle_cep(message)
    else:
        bot.send_message(message.chat.id, "❌ Opa, opa amigão primeiro tu compra o acesso @Webzin116.")

def handle_cpf1(message):
    cpf1 = message.text.replace('/cpf1', '').strip()
    cpf1_api_url = f'https://peopleconsulting.tech/Person/CPF?CPF={cpf1}'
    response = requests.get(cpf1_api_url)

    if response.status_code == 200:
        cpf1_data = response.json()
        process_cpf1_data(cpf1_data, message.chat.id)
    else:
        bot.send_message(message.chat.id, "⚠️ MANUTENÇÃO")

def process_cpf1_data(data, chat_id):
    if data.get('DADOS'):
        dados = data['DADOS'][0]
        cpf = dados.get('CPF', 'RESPOSTA')
        nome = dados.get('NOME', 'RESPOSTA')
        sexo = dados.get('SEXO', 'RESPOSTA')
        nasc = dados.get('NASC', 'RESPOSTA')
        nome_mae = dados.get('NOME_MAE', 'RESPOSTA')
        nome_pai = dados.get('NOME_PAI', 'RESPOSTA')
        est_civil = dados.get('ESTCIV', 'RESPOSTA')
        rg = dados.get('RG', 'RESPOSTA')

        emails = "\n".join([f"{email['EMAIL']}" for email in data.get('EMAIL', [])])

        telefones = "\n".join([f"DDD: '{tel['DDD']}'\nTELEFONE: '{tel['TELEFONE']}'" for tel in data.get('HISTORICO_TELEFONES', [])])

        parentes = "\n".join([f"VINCULO: '{p['VINCULO']}'\nCPF_VINCULO: '{p['CPF_VINCULO']}'" for p in data.get('PARENTES', [])])

        poder_aquisitivo = data.get('PODER_AQUISITIVO', [{}])[0].get('PODER_AQUISITIVO', 'RESPOSTA')
        renda_poder_aquisitivo = data.get('PODER_AQUISITIVO', [{}])[0].get('RENDA_PODER_AQUISITIVO', 'RESPOSTA')
        fx_poder_aquisitivo = data.get('PODER_AQUISITIVO', [{}])[0].get('FX_PODER_AQUISITIVO', 'RESPOSTA')

        enderecos = "\n".join([
            f"LOGR_TIPO: '{end['LOGR_TIPO']}'\nLOGR_NOME: '{end['LOGR_NOME']}'\nLOGR_NUMERO: '{end['LOGR_NUMERO']}'\n"
            f"LOGR_COMPLEMENTO: '{end['LOGR_COMPLEMENTO']}'\nBAIRRO: '{end['BAIRRO']}'\nCIDADE: '{end['CIDADE']}'\n"
            f"UF: '{end['UF']}'\nCEP: '{end['CEP']}'\nDT_ATUALIZACAO: '{end['DT_ATUALIZACAO']}'"
            for end in data.get('ENDERECOS', [])
        ])

        score = data.get('SCORE', [{}])[0]
        csb8 = score.get('CSB8', 'RESPOSTA')
        csb8_faixa = score.get('CSB8_FAIXA', 'RESPOSTA')
        csba = score.get('CSBA', 'RESPOSTA')
        csba_faixa = score.get('CSBA_FAIXA', 'RESPOSTA')

        response_message = (
            f"✅ Consulta Realizada\n\n"
            f"👤 DADOS:\nCPF: '{cpf}'\nNOME: '{nome}'\nSEXO: '{sexo}'\nNASC: '{nasc}'\n"
            f"NOME DA MAE: '{nome_mae}'\nNOME DO PAI: '{nome_pai}'\nESTCIV: '{est_civil}'\nRG: '{rg}'\n\n"
            f"✉️ EMAILs:\n{emails}\n\n"
            f"☎️TELEFONES:\n{telefones}\n\n"
            f"👨‍👩‍👧‍👧 PARENTES:\n{parentes}\n\n"
            f"PODER_AQUISITIVO: '{poder_aquisitivo}'\nRENDA_PODER_AQUISITIVO: '{renda_poder_aquisitivo}'\nFX_PODER_AQUISITIVO: '{fx_poder_aquisitivo}'\n\n"
            f"🏠 ENDERECOS:\n{enderecos}\n\n"
            f"⭐ SCORE:\nCSB8: '{csb8}'\nCSB8_FAIXA: '{csb8_faixa}'\nCSBA: '{csba}'\nCSBA_FAIXA: '{csba_faixa}'\n"
        )

        bot.send_message(chat_id, response_message)
    else:
        bot.send_message(chat_id, "⚠️ MANUTENÇÃO")

def handle_cep(message):
    cep = message.text.replace('/cep', '').strip()
    cep_api_url = f'https://brasilapi.com.br/api/cep/v1/{cep}'
    response = requests.get(cep_api_url)

    if response.status_code == 200:
        cep_data = response.json()
        result_message = (
            f"✅ Consulta Realizada\n\n"
            f"CEP: {cep_data['cep']}\n"
            f"Estado: {cep_data['state']}\n"
            f"Cidade: {cep_data['city']}\n"
            f"Bairro: {cep_data['neighborhood']}\n"
            f"Rua: {cep_data['street']}\n\n"

        )
        bot.send_message(message.chat.id, result_message)
    else:
        bot.send_message(message.chat.id, "⚠️ MANUTENÇÃO")

def handle_cnpj1(message):
    cnpj1 = message.text.replace('/cnpj1', '').strip()
    cnpj1_api_url = f'https://api-publica.speedio.com.br/buscarcnpj?cnpj={cnpj1}'
    response = requests.get(cnpj1_api_url)

    if response.status_code == 200:
        cnpj1_data = response.json()  
        nome_fantasia = cnpj1_data.get("NOME FANTASIA", "")
        razao_social = cnpj1_data.get("RAZAO SOCIAL", "")
        cnpj = cnpj1_data.get("CNPJ", "")
        cnae_descricao = cnpj1_data.get("CNAE PRINCIPAL DESCRICAO", "")
        data_abertura = cnpj1_data.get("DATA ABERTURA", "")
        ddd = cnpj1_data.get("DDD", "")
        telefone = cnpj1_data.get("TELEFONE", "")
        email = cnpj1_data.get("EMAIL", "")
        tipo_logradouro = cnpj1_data.get("TIPO LOGRADOURO", "")
        logradouro = cnpj1_data.get("LOGRADOURO", "")
        numero = cnpj1_data.get("NUMERO", "")
        complemento = cnpj1_data.get("COMPLEMENTO", "")
        bairro = cnpj1_data.get("BAIRRO", "")
        municipio = cnpj1_data.get("MUNICIPIO", "")
        uf = cnpj1_data.get("UF", "")

        # Formate a resposta
        response_message = (
            f"✅ Consulta Realizada\n\n"
            f"🔎 Dados Principais\n\n"
            f"Nome: {nome_fantasia}\n"
            f"CPF: {razao_social}\n"
            f"CNPJ: {cnpj}\n"
            f"DESCRICAO: {cnae_descricao}\n"
            f"ABERTURA EM: {data_abertura}\n\n"
            f"☎️ Numeros:\n"
            f"DDD: {ddd}\n"
            f"TELEFONE: {telefone}\n\n"
            f"EMAIL: {email}\n\n"
            f"🏠 Endereços\n"
            f"LOGRADOURO: {tipo_logradouro} {logradouro}\n"
            f"NUMERO: {numero}\n"
            f"COMPLEMENTO: {complemento}\n"
            f"BAIRRO: {bairro}\n"
            f"MUNICIPIO: {municipio}\n"
            f"UF: {uf}\n\n"
        )

        bot.send_message(message.chat.id, response_message)
    else:
        bot.send_message(message.chat.id, "⚠️ MANUTENÇÃO VOLTE MAIS TARDE")

def handle_cpf2(message):
    cpf2 = message.text.replace('/cpf2', '').strip()
    cpf2_api_url = f'https://peopleconsulting.tech/Person/CPF?CPF={cpf2}'
    response = requests.get(cpf2_api_url)

    if response.status_code == 200:
        cpf2_data = response.json()
        bot.send_message(message.chat.id, f"✅ Consulta Realizada(sem modelação)\n\n{cpf2_data}")
    else:
        bot.send_message(message.chat.id, f"⚠️ MANUTENÇÃO")


def handle_tel1(message):
    tel1 = message.text.replace('/tel1', '').strip()
    tel1_api_url = f'https://peopleconsulting.tech/Person/phoneNumber?phoneNumber={tel1}'
    response = requests.get(tel1_api_url)

    if response.status_code == 200:
        tel1_data = response.json()
        process_tel1_data(tel1_data, message.chat.id)
    else:
        bot.send_message(message.chat.id, "⚠️ MANUTENÇÃO")

def process_tel1_data(data, chat_id):
    for entry in data:
        dados = entry.get('DADOS', [{}])[0]
        cpf = dados.get('CPF', 'RESPOSTA')
        nome = dados.get('NOME', 'RESPOSTA')
        sexo = dados.get('SEXO', 'RESPOSTA')
        nasc = dados.get('NASC', 'RESPOSTA')
        nome_mae = dados.get('NOME_MAE', 'RESPOSTA')
        nome_pai = dados.get('NOME_PAI', 'RESPOSTA')
        est_civil = dados.get('ESTCIV', 'RESPOSTA')
        rg = dados.get('RG', 'RESPOSTA')
        titulo_eleitor = dados.get('TITULO_ELEITOR', 'RESPOSTA')

        emails = "\n".join([f"'{email['EMAIL']}'" for email in entry.get('EMAIL', [])])

        telefones = "\n".join([f"DDD: '{tel['DDD']}'\nTELEFONE: '{tel['TELEFONE']}'" for tel in entry.get('HISTORICO_TELEFONES', [])])

        parentes = "\n".join([f"VINCULO: '{p['VINCULO']}'\nCPF_VINCULO: '{p['CPF_VINCULO']}'" for p in entry.get('PARENTES', [])])

        enderecos = "\n".join([
            f"LOGR_TIPO: '{end['LOGR_TIPO']}'\nLOGR_NOME: '{end['LOGR_NOME']}'\nLOGR_NUMERO: '{end['LOGR_NUMERO']}'\n"
            f"LOGR_COMPLEMENTO: '{end['LOGR_COMPLEMENTO']}'\nBAIRRO: '{end['BAIRRO']}'\nCIDADE: '{end['CIDADE']}'\n"
            f"UF: '{end['UF']}'\nCEP: '{end['CEP']}'\nDT_ATUALIZACAO: '{end['DT_ATUALIZACAO']}'"
            for end in entry.get('ENDERECOS', [])
        ])

        response_message = (
            f"✅ Consulta Realizada\n\n"
            f"👤 DADOS:\nCPF: '{cpf}'\nNOME: '{nome}'\nSEXO: '{sexo}'\nNASC: '{nasc}'\n"
            f"NOME DA MAE: '{nome_mae}'\nNOME DO PAI: '{nome_pai}'\nESTCIV: '{est_civil}'\nRG: '{rg}'\n"
            f"TITULO DE ELEITOR: '{titulo_eleitor}'\n\n"
            f"✉️ EMAILs:\n{emails}\n\n"
            f"☎️ TELEFONES:\n{telefones}\n\n"
            f"👨‍👩‍👧‍👧 PARENTES:\n{parentes}\n\n"
            f"🏠 ENDERECOS:\n{enderecos}\n\n"
        )

        bot.send_message(chat_id, response_message)
    else:
        bot.send_message(message.chat.id, "⚠️ MANUTENÇÃO")


def handle_tel2(message):
    tel2 = message.text.replace('/tel2', '').strip()
    tel2_api_url = f'https://mdzapis.online/api/consultas?type=tel1&query={tel2}&apitoken=mdzup800'
    response = requests.get(tel2_api_url)

    if response.status_code == 200:
        tel2_data = response.json()
        resultado = tel2_data.get('resultado', 'Não foi possÃ­vel obter um resultado.')

        bot.send_message(message.chat.id, f"Resultado da Consulta\n{resultado}")
    else:
        bot.send_message(message.chat.id, f"⚠️ MANUTENÇÃO")

def handle_placa(message):
        placa = message.text.replace('/placa', '').strip()
        placa_api_url = f'https://mdzapis.online/api/consultas?type=placa2&query={placa}&apitoken=mdzup800'
        response = requests.get(placa_api_url)

        if response.status_code == 200:
            placa_data = response.json().get('resultado', 'Nenhum resultado.')
            bot.send_message(message.chat.id, f"Consulta da Placa {placa} realizada\n{placa_data}")
        else:
            bot.send_message(message.chat.id, f"API off")

def handle_nome(message): 
    nome = message.text.replace('/nome', '').strip()
    nome_api_url = f'https://mdzapis.online/api/consultas?type=nome&query={nome}&apitoken=mdzup800'
    response = requests.get(nome_api_url)

    if response.status_code == 200:
        result_json = response.json()
        resultado = result_json.get('resultado', 'Nenhum resultado disponÃ­vel.')
        bot.send_message(message.chat.id, f"Resultado da consulta do nome {nome}:\n{resultado}")
    else:
        bot.send_message(message.chat.id, f"off.")


def show_menu(message):
    user_name = get_user_name(message)
    menu_message = (
        f"Opa {user_name} ! 🎉\n"
        "Esse é meu menu de consultas.\n\n"
        "🔎 CONSULTAS -\n\n"
        "🪪 CPF:\n"
        "➔ /cpf1\n"
        "➔ /cpf2 base (simples)\n\n"
        "👨‍💼 CNPJ:\n"
        "➔ /cnpj1\n"
        "➔ /cnpj2 \n\n"
        "🏠 CEP:\n"
        "/cep\n\n"
        "👤 NOME:\n"
        "➔ /nome\n\n"
        "🚘 PLACA:\n"
        "➔ /placa\n\n"
        "☎️ TELEFONE:\n"
        "➔/tel1\n"
        "➔ /tel2 base (Claro)\n\n"
        "🤖 IAs -\n\n"
        "GPT:\n"
        "➔ /ia"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton('Atualizações 🎉', url='https://t.me/+ar4YCS8H1QI1YzNh')],
    ])

    bot.send_message(message.chat.id, menu_message, reply_markup=buttons)


    bot.send_message(message.chat.id, me_message, reply_markup=buttons)

    buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton('Dono', url='https://t.me/Webzin116')],
    buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton('Suporte', url='https://t.me/martisz777')]
])

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    handle_messages(message)

if __name__ == "__main__":
    app.run()





