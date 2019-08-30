# FGBR Discord Bot

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from datetime import datetime
import urllib.request
import lxml.etree as etree
import logging
import sys
import os
from os import path

###################################
# 
# UTILITIES #
def isDM(channel):
    return (isinstance(channel, discord.DMChannel) or isinstance(channel, discord.GroupChannel))

def console_log (ctx, text):
    now = datetime.utcnow().strftime('%x %X')
    if ctx != None and isDM(ctx.message.channel) == True:
        log_message = f'{ctx.message.author.name}#{ctx.message.author.discriminator} - {text} <None:private> - {now}'
    elif ctx != None:
        log_message = f'{ctx.message.author.name}#{ctx.message.author.discriminator} - {text} <{ctx.message.channel.name}:{ctx.message.guild.name}> - {now}'
    elif ctx == None:
        log_message = text
    print(log_message)
    logging.debug(log_message)

def url_request_content(url):
    return urllib.request.urlopen(url).read()
###################################

###################################
# 
# SETUP #

bot = commands.Bot(command_prefix='!fgbr:')
bot.remove_command('help')

# Get env vars
BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))
BOT_AIS_KEY = str(os.environ.get('BOT_AIS_KEY'))
BOT_AIS_TOKEN = str(os.environ.get('BOT_AIS_TOKEN'))

# brazilian charts
charts_types = [ ['ADC','Carta de Aérodromo'] , ['IAC', 'Carta de Aproximação por Instrumentos'], ['PDC', 'Carta de Estacionamento de Aérodromo'], ['SID', 'Carta de Saída Normalizada - IFR'], ['STAR', 'Carta de Chegada Normalizada - IFR'], ['VAC', 'Carta de Aproximação Visual - VFR'] ]
charts_types_string = '\n'
for chart_type in charts_types:
    charts_types_string += f'{chart_type[0]} : {chart_type[1]}\n'

# logging
if path.exists('log.log'):
    try:
        os.remove('log_old.log')        
    except:
        pass
    os.rename('log.log', 'log_old.log')
logging.basicConfig(filename='log.log',level=logging.DEBUG)

console_log(None, f'Discord Python API v{discord.__version__}\nPython {sys.version}\n{os.popen("pip freeze").read()}')
###################################

###################################
# 
# EVENTS #

@bot.event
async def on_ready():
    print ('Bot autenticado com sucesso!', f'\nMeu nome: {bot.user.name}#{bot.user.discriminator}', f'\nMeu ID: {bot.user.id}')

    guilds_name = ''
    for guild in bot.guilds:
        guilds_name += f'<{guild.name}>'

    print (f'Servidores: {len(bot.guilds)} ({guilds_name})\n', '#'*20,'\n')
    
    game = discord.Game(name='Digite: !fgbr:ajuda para saber os comandos', type=2)
    await bot.change_presence(activity=game)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        #await bot.send_typing(ctx.message.channel) # enable display of typing symbol in discord 
        #await asyncio.sleep(1)
        await ctx.send('***Erro***: Este comando não pode ser usado em mensagens privadas.\n:x:')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send('***Erro***: Comando desabilitado.\n:x:')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f'***Erro***: Comando não existente. Verifique o comando digitado.\nDigite {bot.command_prefix}ajuda para saber os comandos.\n:x:')
        console_log(ctx, f'(CommNotFound: {ctx.message.content})')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('***Erro***: Algumas informações deste comando estão faltando.\nVerifique se o comando foi digitado corretamente.\n:x:')
###################################

###################################
# 
# COMMANDS #

@bot.command()
async def ajuda(ctx):
    await ctx.send(f'***Comandos***:\n\n**{bot.command_prefix}info @usuario**: Mostra informações sobre um usuário.\n**{0}serverinfo**: Exibe informações sobre o servidor.\n**{bot.command_prefix}carta icao tipo_de_carta**: Exibe cartas aéronauticas do aéroporto especificado.\n**{bot.command_prefix}ajuda**: Exibe este texto de ajuda.')
    console_log(ctx, '(/ajuda)')

@bot.command()
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title=f'Perfil de: {user.name}', description='Aqui está o que eu pude encontrar.', color=0x00ff00)
    embed.add_field(name='Nome', value=user.name, inline=True)
    embed.add_field(name='ID', value=user.id, inline=True)
    embed.add_field(name='Status', value=user.status, inline=True)
    embed.add_field(name='Cargo mais alto', value=user.top_role)
    d = datetime.strptime(f'{user.joined_at}'.split('.')[0], '%Y-%m-%d %H:%M:%S')
    months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    embed.add_field(name='Entrou em', value=f'{d.day} de {months[d.month-1]} de {d.year} as {d.hour-3}h {d.minute}m {d.second}s')
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)
    console_log(ctx, f'(/info:{user.name})')
@info.error
async def info_error(ctx, error):
    await ctx.send(f'***Erro***: Certifique de ter digitado o nome do usuário\n***Uso correto***: {bot.command_prefix}info @nome')

@bot.command()
async def serverinfo(ctx):
    if not isDM(ctx.message.channel):
        embed = discord.Embed(name=f'{ctx.message.guild.name}\'s info', description='Aqui está o que eu pude encontrar.', color=0x00ff00)
        embed.set_author(name=f'Informações do Servidor: {ctx.message.guild.name}')
        embed.add_field(name='ID', value=ctx.message.guild.id, inline=True)
        embed.add_field(name='Cargos', value=len(ctx.message.guild.roles), inline=True)
        embed.add_field(name='Membros', value=len(ctx.message.guild.members))
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)
    console_log(ctx, '(/serverinfo)')

@bot.command()
async def carta(ctx, icao : str, tipo : str):
    icao = icao.upper()
    tipo = tipo.upper()
    embed = discord.Embed(title='Resultado(s) da pesquisa:', description='Aqui está o que eu pude encontrar.', color=0xF35EFF)
    embed.set_footer(text='dados cedidos por Aisweb')
    embed.set_author(name=f'Procurando cartas {tipo} de ***{icao}***')
    embed.set_thumbnail(url='https://bunkr-private-prod.s3.amazonaws.com/8/a/e/8aed7d70-aa7a-4744-ad31-2b16ad729ab7_orig.jpg')
    tipo_correto = False
    for chart_type in charts_types:
        if tipo == chart_type[0]:
            tipo_correto = True
    if tipo_correto == False:   
        embed.add_field(name='Oops. Tipo de Carta Incorreto', value=f'Verifique o Tipo de Carta digitado.\n\nTipos Aceitos: {charts_types_string}\nExemplo: {bot.command_prefix}carta SBGR ADC')
    content = url_request_content(f'http://www.aisweb.aer.mil.br/api/?apiKey={BOT_AIS_KEY}&apiPass={BOT_AIS_TOKEN}&area=cartas&IcaoCode={icao}&tipo={tipo}')
    tree = etree.fromstring(content)
    for item in tree.iter('item'):
        embed.add_field(name=item.find('nome').text, value=item.find('link').text.split(';')[0], inline=True)
    if len(embed.fields) == 0:
        embed.add_field(name='Oops. Não encontrei nada', value='Verifique o ICAO digitado (só possuimos suporte a aeroportos brasileiros).')
    await ctx.send(embed=embed)
    console_log(ctx, f'(/carta:{icao}:{tipo})')
@carta.error
async def carta_error(error, ctx):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        return await ctx.send(f'***Erro***: Certifique-se de ter digitado o ICAO e o tipo de carta corretamente.\n\nTipos Aceitos: {charts_types_string}\nExemplo: {bot.command_prefix}carta SBGR ADC')
###################################

bot.run(BOT_TOKEN)