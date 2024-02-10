import discord
from discord.ext import commands
from model import get_class
import os, random
import requests

# Configura el token de tu bot de Discord
TOKEN = 'TOKEN'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(get_class(model_path="./keras_model.h5", labels_path="./labels.txt", image_path=f"./{attachment.filename}"))
    else:
        await ctx.send("You forgot to upload the image :(")

@bot.event
async def on_message(message):
    # Verificar que el mensaje tiene archivos adjuntos
    if message.attachments:
        for attachment in message.attachments:
            # Verificar que el archivo adjunto es una imagen
            if attachment.content_type.startswith('image'):
                # Guardar la imagen localmente
                file_path = f"./{attachment.filename}"
                await attachment.save(file_path)
                # Obtener la clasificación de la imagen
                classification = get_class(model_path="./keras_model.h5", labels_path="./labels.txt", image_path=file_path)
                # Enviar la clasificación en el mismo canal del mensaje original
                await message.channel.send(f"La imagen fue clasificada como: {classification}")
                # Eliminar la imagen local después de procesarla
                os.remove(file_path)
                # Borrar el mensaje original
                await message.delete()
    # Continuar procesando otros eventos de mensaje
    await bot.process_commands(message)

# Ejecutar el bot con el token
bot.run(TOKEN)
