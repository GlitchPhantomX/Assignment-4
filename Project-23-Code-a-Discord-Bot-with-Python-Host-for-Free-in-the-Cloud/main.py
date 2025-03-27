import discord
from discord.ext import commands
import asyncio
import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    case_insensitive=True,
    help_command=None
)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print(f'Connected to {len(bot.guilds)} servers')
    print('------')
    
    # Set custom status
    activity = discord.Activity(
        name="!help for commands",
        type=discord.ActivityType.listening
    )
    await bot.change_presence(activity=activity)

# Basic command with error handling
@bot.command(name='hello', help='Greets the user')
async def hello(ctx):
    try:
        await ctx.send(f'Hello {ctx.author.mention}! How can I help you today?')
    except Exception as e:
        print(f"Error in hello command: {e}")
        await ctx.send("Oops! Something went wrong.")

# Server info command
@bot.command(name='serverinfo', help='Displays server information')
async def server_info(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"Server Info: {guild.name}",
        description=f"Created at: {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

# Custom help command
@bot.command(name='help', help='Shows available commands')
async def custom_help(ctx):
    embed = discord.Embed(
        title="Bot Commands Help",
        description="Here are the available commands:",
        color=discord.Color.green()
    )
    
    for command in bot.commands:
        embed.add_field(
            name=f"!{command.name}",
            value=command.help or "No description available",
            inline=False
        )
    
    await ctx.send(embed=embed)

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Try !help for available commands.")
    else:
        print(f"Error occurred: {error}")
        await ctx.send("An error occurred while executing that command.")

# Run the bot
try:
    with open('bot_token.txt', 'r') as f:
        token = f.read().strip()
except FileNotFoundError:
    token = input("Enter your Discord bot token: ")
    with open('bot_token.txt', 'w') as f:
        f.write(token)

if __name__ == "__main__":
    print("Starting bot...")
    bot.run(token)