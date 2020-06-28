import googlemaps
from timezonefinder import TimezoneFinder
import discord
from discord.ext import commands
import arrow as ar
import os
import settings
from discord.utils import find
import json
import sys
from master import get_prefix
from master import get_color

asciiString = """
                        .s$$$Ss.
            .8,         $$$. _. .              ..sS$$$$$"  ...,.;
 o.   ,@..  88        =.$"$'  '          ..sS$$$$$$$$$$$$s. _;"'
  @@@.@@@. .88.   `  ` ""l. .sS$$.._.sS$$$$$$$$$$$$S'"'
   .@@@q@@.8888o.         .s$$$$$$$$$$$$$$$$$$$$$'
     .:`@@@@33333.       .>$$$$$$$$$$$$$$$$$$$$'
     .: `@@@@333'       ..>$$$$$$$$$$$$$$$$$$$'
      :  `@@333.     `.,   s$$$$$$$$$$$$$$$$$'
      :   `@33       $$ S.s$$$$$$$$$$$$$$$$$'
      .S   `Y      ..`  ,"$' `$$$$$$$$$$$$$$
      $s  .       ..S$s,    . .`$$$$$$$$$$$$.
      $s .,      ,s ,$$$$,,sS$s.$$$$$$$$$$$$$.
      / /$$SsS.s. ..s$$$$$$$$$$$$$$$$$$$$$$$$$.
     /`.`$$$$$dN.ssS$$'`$$$$$$$$$$$$$$$$$$$$$$$.
    ///   `$$$$$$$$$'    `$$$$$$$$$$$$$$$$$$$$$$.
   ///|     `S$$S$'       `$$$$$$$$$$$$$$$$$$$$$$.
  / /                      $$$$$$$$$$$$$$$$$$$$$.
                           `$$$$$$$$$$$$$$$$$$$$$s.
                            $$$"'        .?T$$$$$$$
                           .$'        ...      ?$$#\
                           !       -=S$$$$$s
                         .!       -=s$$'  `$=-_      :
                        ,        .$$$'     `$,       .|
                       ,       .$$$'          .        ,
                      ,     ..$$$'
                          .s$$$'                 `s     .
                   .   .s$$$$'                    $s. ..$s
                  .  .s$$$$'                      `$s=s$$$
                    .$$$$'                         ,    $$s
               `   " .$$'                               $$$
               ,   s$$'                              .  $$$s
            ` .s..s$'                                .s ,$$
             .s$$$'                                   "s$$$,
          -   $$$'                                     .$$$$.
        ."  .s$$s                                     .$',',$.
        $s.s$$$$S..............   ................    $$....s$s......
"""

bot = commands.Bot(command_prefix=get_prefix)
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
bot.remove_command("help")
tf = TimezoneFinder()

month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]

guildCount: int
memberCount: int

startup_extensions = [
    "listener.listener",
    "listener.timeZone",
    "listener.reminder",
    "listener.distance",
    "listener.timer",
    "listener.currency",
    "listener.botCommands",
    "listener.jokes",
    "listener.birthday"
]

# On bot login, send info
@bot.event
async def on_ready():
    bot.remove_command('help')
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    print('\nLogged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print(asciiString)
    await bot.change_presence(activity=discord.Game(name="the Voight Kampff test"))

@bot.event
async def on_guild_join(guild):
    with open('files/{}.json'.format(guild.id), 'w+') as f:
        startData = {"info":{"prefix" : ".", "color" : "0x176BD3"}}
        json.dump(startData, f, indent = 4)
    embed = discord.Embed(title="Joined!", colour=discord.Colour(1534931))
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        embed.add_field(name="What's up!", value="Hello {}! I'm Timely. \nThank you for adding me to your server. Type in `.help` for commands, or `.timeprefix PREFIX` to change your prefix.".format(guild.name))
        await general.send(embed=embed)
    username = "Timely [.]"
    await bot.user.edit(username=username)

        
@bot.event
async def on_guild_remove(guild):
    os.remove("files/{}.json".format(guild.id))
    print("deleted:" + str(guild.id))

@bot.command()
async def PPstatusPP(ctx, *args):
    if ctx.author.id == 524251122823856149:
        text = " ".join(args)
        await bot.change_presence(activity=discord.Game(name=text))
        user = bot.get_user(524251122823856149)
        await user.send(""""Current statistics:
                        Users: {0}
                        Guilds: {1}""".format(memberCount, guildCount))

@bot.event
async def on_command_error(ctx, exception):
    color = get_color(bot, ctx.message)
    if type(exception) == discord.ext.commands.errors.CommandNotFound:
        embed = discord.Embed(title="**Command Error >:(**", colour = discord.Color(color))
        prefix = get_prefix(bot, ctx.message)
        embed.add_field(name = "That's not a recognized command!", value = "Please try again. \nType `{0}help` for help!".format(prefix))
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title="**Command Error >:(**", colour = discord.Color(color))
        prefix = get_prefix(bot, ctx.message)
        embed.add_field(name = "There's been some kind of error!", value = "Please try again. \nType `{0}help` for help!".format(prefix))
        await ctx.send(embed = embed)

@bot.event
async def on_error(event_method, *args, **kwargs):
    id = (args[0].id)
    error = sys.exc_info()
    if error[0] == FileNotFoundError:
        with open('files/{}.json'.format(id), 'w+') as f:
            startData = {"info":{"prefix" : ".", "color" : "0x176BD3"}}
            json.dump(startData, f, indent = 4)

@bot.command()
async def contact(ctx, *args):
    text = " ".join(args)
    date = ar.utcnow().format()
    string = "Message from `{0}`, from guild `{1}`, ID: `{2}`. Sent at `{3}`. Message states: \n`{4}`.".format(ctx.message.author, ctx.guild.name, ctx.guild.id, date, text)
    user = bot.get_user(524251122823856149)
    await user.send(string)

# Run, bot, run!
bot.run(token)
