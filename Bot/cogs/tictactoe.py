from discord.ext import commands
import discord
from discord.ext.commands.errors import BadArgument

class tictactoe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.winning_opt = ([0,1,2], [3,4,5], [6,7,8], [0,4,8], [2,4,6], [0,3,6], [1,4,7], [2,5,8])
        self.is_over = True
        self.turn = True
        self.poles = [':white_large_square:'] * 9
        self.player1 = None
        self.player2 = None

    async def _send_poles(self, context):
        return await context.send(f'{self.poles[0]} {self.poles[1]} {self.poles[2]}\n{self.poles[3]} {self.poles[4]} {self.poles[5]}\n{self.poles[6]} {self.poles[7]} {self.poles[8]}')

    @commands.command()
    async def tictactoe(self, context, member : discord.Member):
        if self.is_over == False: return await context.send("Someone's are playing right now. Please be patient and wait for them to finish.")
        elif member == context.author: return await context.send('You can\'t play with only yourself. Go find some friends.')
        else: 

            if self.player1 == None: self.player1 = context.author
            if self.player2 == None: self.player2 = member

            await self._send_poles(context)

            self.is_over = False

    @commands.command()
    async def chose(self, context, pole):
        if self.is_over == True:
            return await context.send('First start the game!')

        try:
            pole = int(pole)
            if pole < 1 or pole > 9:
                return await context.send('Wrong value! Chose between 1 and 9.')
        except:
            return await context.send('Wrong value! Only numbers are accepted')

        if self.poles[pole-1] != ':white_large_square:':
            return await context.send('This pole is taken. Chose another!')

        if context.author == self.player1:
            if self.turn == True:
                self.turn = False
                self.poles[pole-1] = ':regional_indicator_x:'
                await self._send_poles(context)
            else:
                await context.send('Wait for your trun!')
        elif context.author == self.player2:
            if self.turn == False:
                self.turn = True
                self.poles[pole-1] = ':o2:'
                await self._send_poles(context)
            else:
                await context.send('Wait for your trun!')
        else:
            await context.send('Don\'t interupt when others are playing!')

        for option in self.winning_opt:
            if self.poles[option[0]] == ':white_large_square:': continue 
            if self.poles[option[0]] == self.poles[option[1]] == self.poles[option[2]]:
                if self.poles[option[0]] == ':regional_indicator_x:':
                    await context.send(f"The winner is {str(self.player1)[:-5]}")
                else:
                    await context.send(f"The winner is {str(self.player2)[:-5]}")
                self.is_over = True
                self.poles = [':white_large_square:'] * 9

    @commands.command()
    async def quit(self, context):
        if context.author in (self.player1, self.player2):
            self.is_over = True
            self.poles = [':white_large_square:'] * 9
            return await context.send('The game was aborted!')
        return await context.send('You can\'t cancel the game!')


def setup(client):
    client.add_cog(tictactoe(client))