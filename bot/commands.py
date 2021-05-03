#AUTHOR: duhack
#GITHUB: https://github.com/duhack

import discord
import time
import datetime
import mysql.connector
from discord.ext import commands
from discord.utils import get

embedColor = 0x0047b3 # KOLOR WYSYŁANYCH WIADOMOŚCI

configMysql = {
    'user': '', #uzytkownik bazy danych
    'password': '', #haslo do bazy danych
    'host': '', #ip bazy danych
    'database': '', #baza danych
}
rankSynchro = 832616480339394640 # id nadawanej rangi na discordzie (do wyciągnięcia przez tryb developerski)


connection = mysql.connector.connect(**configMysql)
cursor = connection.cursor()

start_time = time.time()

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def synchronizacja(self, ctx, code = None):
        embed = None
        if code is not None:
            sql_select_Query = "select * from `synchronizacja-dsc` WHERE code='"+code+"'"
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            znaleziono = False
            for row in records:
                znaleziono = True
                if str(row[2]) == "nie":
                    cursor.execute("select `nick` from players WHERE uid='"+str(row[0])+"'")
                    records_nick = cursor.fetchall()
                    member = ctx.author
                    avatar = str(member.avatar_url)
                    role = get(member.guild.roles, id=rankSynchro)
                    await member.add_roles(role)
                    embed = discord.Embed(title="Synchronizacja konta", description="Synchronizacja konta przebiegła prawidłowo, otrzymujesz rangę Zweryfikowany.", color=embedColor)
                    embed.add_field(name="Serwer", value=records_nick[0][0])
                    embed.add_field(name="Discord", value=member)
                    embed.set_thumbnail(url=avatar)
                    sql = "UPDATE `synchronizacja-dsc` SET used = %s, account_discord = %s, avatar = %s WHERE code=%s"
                    val = ("tak", member.id, str(member.avatar_url)[0:-15]+'.png?size=1024', code)
                    cursor.execute(sql, val)
                    connection.commit()
                else:
                    embed = discord.Embed(title="Synchronizacja konta", description="Ten klucz został już zrealizowany!", color=embedColor)
            if znaleziono == False:
                embed = discord.Embed(title="Synchronizacja konta", description="Podany kod jest nieprawidłowy!", color=embedColor)
            cursor.close()
        else:
            embed = discord.Embed(title="Synchronizacja konta", description="Aby użyć tej komendy wykonaj wygeneruj klucz w grze (**/discord**),\n \n a następnie wpisz go w tej formie: **!synchronizacja <KOD>**\n \n Aby sprawdzić status twojej synchronizacji - użyj komendy w grze (**/discord-status**)", color=embedColor)
        if not embed == None:
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))