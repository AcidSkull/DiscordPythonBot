from discord.ext import commands
import discord

class Members(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('\033[92m' + 'Bot is ready!' + '\033[0m')
        await self.client.change_presence(activity=discord.Game('Minecraft 2'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            embedVar = discord.Embed(
                title=f'Welcome {member}!',
                description=f'It is nice to greet you to {member.guild}. Remeber to be respectfull to another or we send you to the window of life.',
                color=0x0efbe0)
            embedVar.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=embedVar)

    @commands.command()
    async def ping(self, context):
        await context.send('Pong!')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member : discord.Member, *, reason=' unknown reasone'):
        await member.kick(reason=reason)
        await context.send(f'User {member} has been kicked for {reason}.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member : discord.Member, *, reason=' unknown reasone'):
        print(reason)
        await member.ban(reason=reason)
        await context.send(f'User {member} has been ban for {reason}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, context, *, member):
        banned_users = await context.guild.bans()
        member_name, member_discriminator = member.split("#")

        for entry in banned_users:
            user = entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await context.guild.unban(user)
                await context.send(f'User {user.mention} has been unbaned.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, context, member : discord.Member, *, role : discord.Role ):
        await member.add_roles(role)
        await context.send(f'User {member} has been promoted to {role}.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, context, member : discord.Member, *, role : discord.Role):
        await member.remove_roles(role)
        await context.send(f'User {member} has been degraded from {role}')
        
def setup(client):
    client.add_cog(Members(client))