from discord.ext import commands
import discord, youtube_dl

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, context, url : str, voice_channel='Music'):
        channel = discord.utils.get(context.guild.voice_channels, name=voice_channel)
        voice = discord.utils.get(self.client.voice_clients, guild=context.guild)
        if voice == None:
            await channel.connect()
        else:
            await context.send('Bot is connectedd to another channel.', delete_after=10)

    @commands.command()
    async def leave(self, context):
        voice = discord.utils.get(self.client.voice_clients, guild=context.guild)
        if voice == None:
            await context.send('Bot is not connected to any channel so it can\'t leave.', delete_after=10)
        else:
            await voice.disconnect()

def setup(client):
    client.add_cog(Music(client))