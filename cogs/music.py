from discord.errors import ClientException
from discord.ext import commands
import discord, youtube_dl, os

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, context, url : str, voice_channel='Music'):
        music = os.path.isfile('music.mp3')
        try:
            if music:
                os.remove('music.mp3')
        except PermissionError:
            await context.send('Wait for the current playing music to end.')
            return
        
        channel = discord.utils.get(context.guild.voice_channels, name=voice_channel)
        try:
            await channel.connect()
        except ClientException:
            pass
        voice_client = discord.utils.get(self.client.voice_clients, guild=context.guild)
        
        ydl_opts = {
            'format' : 'bestaudio/best',
            'postprocessors' : [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec' : 'mp3',
                'preferredquality' : '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir('./'):
            if file[-4:] == '.mp3':
                os.rename(file, 'music.mp3')
        voice_client.play(discord.FFmpegPCMAudio('music.mp3'))

    @commands.command()
    async def leave(self, context):
        voice_client = discord.utils.get(self.client.voice_clients, guild=context.guild)
        if voice_client == None:
            await context.send('Bot is not connected to any channel so it can\'t leave.')
        else:
            await voice_client.disconnect()

    

def setup(client):
    client.add_cog(Music(client))