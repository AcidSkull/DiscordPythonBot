from discord.ext.commands.errors import RoleNotFound
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import os, discord

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=";", intents=intents)

@client.command()
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')

@client.event
async def on_command_error(context, error):
    if isinstance(error, MissingPermissions):
        await context.send('You have no perrmissions to runn this command!')
    elif isinstance(error, RoleNotFound):
        await context.send('This role dont\'t exist.')
    else:
        raise error

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

load_dotenv()
client.run(os.getenv('API_KEY'))
