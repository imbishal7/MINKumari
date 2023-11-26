import discord
import os
import asyncio
from discord.ext import commands
from pytz import timezone
import ast
import inspect

from stay_awake import stay_awake
from greet import greet_user
from quote import get_quote
from tabulate import tabulate
from aops import give_category, give_contest, give_sub_contest, give_problem, give_solution, random_prob

from image_from_htm import get_image_from_html

from wc_func_v2 import add_weekly_challenge, check_solution, get_leaderboard, send_wc, delete_weekly_challenge, add_to_wc_solvers, get_all_wc_solvers, remove_all_from_wc_solvers, update_leaderboard, add_to_wc_solvers

import datetime
from datetime import timedelta

token = os.environ['token']
nepal_timezone = timezone('Asia/Kathmandu')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


def has_role(role_name):

  def predicate(ctx):
    if ctx.author is None:
      return False
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    return role is not None and role in ctx.author.roles

  return commands.check(predicate)


bot = commands.Bot(command_prefix='>', intents=intents)

bot.remove_command('help')

help_commands_order = [
  'greet', 'motivate', 'category', 'contest', 'subcontest', 'random', 'gimme',
  'helpme', 'wc', 'leaderboard', 'set_weekly_challenge', 'del_weekly_challenge'
]


@bot.command()
async def help(ctx, command_name=None):
  if command_name is None:
    embed = discord.Embed(title="MIN Kumari's All Available Commands",
                          color=discord.Color.green())
    for command_name in help_commands_order:
      command = bot.get_command(command_name)
      if command:
        embed.add_field(name=command.name,
                        value=command.description,
                        inline=False)
    await ctx.send(embed=embed)
  else:
    command = bot.get_command(command_name)
    if command is None:
      await ctx.send(f"Command '{command_name}' not found.")
    else:
      embed = discord.Embed(title=f"Command: {command.name}",
                            color=discord.Color.gold())
      embed.add_field(name='Description',
                      value=command.description,
                      inline=False)

      signature = f"{command.name} {command.signature}"
      docstring = inspect.getdoc(command.callback)
      if docstring:
        usage = docstring.strip().split('\n')[0].replace('Usage: ', '')
        embed.add_field(name='Usage', value=usage, inline=False)
      else:
        embed.add_field(name='Usage', value=signature, inline=False)

      await ctx.send(embed=embed)


async def welcome(member):
  channel = member.guild.system_channel
  if channel is not None:
    await channel.send(greet_user(member.mention))
    role_id = 1080148435577098260
    mk_id = 1110416559094116402

    role = bot.get_channel(role_id).mention
    mk = bot.get_channel(mk_id).mention

    welcome_msg = f"""Welcome to MIN's official Discord server. You can ask your math related queries in problem discussion channels and if your are interested in Olympiads you can checkout my available commands, and try them out at {mk}. Also, please assign yourself with the roles from {role}."""
    await channel.send(welcome_msg)


@bot.event
async def on_member_join(member):
  await welcome(member)


@bot.command(
  description='Greets everyone, unless specified, with a random greeting')
async def greet(ctx, username='everyone'):
  """
  Usage: >greet <@someone>
  """

  role_id = 1080148435577098260
  mk_id = 1110416559094116402

  role = bot.get_channel(role_id).mention
  mk = bot.get_channel(mk_id).mention

  welcome_msg = f"""Welcome to MIN's official Discord server. You can ask your math related queries in problem discussion channels and if your are interested in Olympiads you can checkout my available commands, and try them out at {mk}. Also, please assign yourself with the roles from {role}."""
  await ctx.send(greet_user(username))
  await ctx.send(welcome_msg)


@bot.command(description='Sends a random motivating quote.')
async def motivate(ctx):
  """Usage: >motivate"""
  await ctx.send(get_quote())


@bot.command(
  description='Lists all available categories of contests and competitions.')
async def category(ctx):
  """Usage: >category"""
  result = give_category()
  table_data = [[item] for item in result]
  table = tabulate(table_data, headers=['Categories'], tablefmt='grid')

  embed = discord.Embed(title="All Available Categories",
                        description=f"```{table}```",
                        color=discord.Color.blue())
  await ctx.channel.send(embed=embed)


@bot.command(
  description='Lists all available contests for a specific category')
async def contest(ctx, *, category):
  """Usage: >contest <category>"""
  name = category
  try:
    result = give_contest(name)
    num_columns = 3

    table_data = [
      result[i:i + num_columns] for i in range(0, len(result), num_columns)
    ]

    table = tabulate(table_data, tablefmt='plain')
    table_chunks = [table[i:i + 1000] for i in range(0, len(table), 1000)]

    for chunk in table_chunks:
      await ctx.send(f'```\n{chunk}\n```')
  except:
    await ctx.send(
      'Category Missing. Enter one category from the available ones.')


@bot.command(
  description='Lists all available events or subcontests for specified contest.'
)
async def subcontest(ctx, *, contest):
  """Usage: >subcontest <contest>"""
  name = contest
  try:
    result = give_sub_contest(name)

    num_columns = 3

    table_data = [
      result[i:i + num_columns] for i in range(0, len(result), num_columns)
    ]
    table = tabulate(table_data, tablefmt='plain')
    table_chunks = [table[i:i + 1000] for i in range(0, len(table), 1000)]

    for chunk in table_chunks:
      await ctx.send(f'```\n{chunk}\n```')
  except:
    await ctx.send(
      'Contest Missing. Enter one contest from the available ones.')


@bot.command(
  description=
  "Fetches a random problem or from specified category, contest, or name from the database of 36532 unique problems"
)
async def random(ctx, *, query=None):
  """Usage: >random
            >random <category/contest/subcontest>
  """

  name = query
  try:
    result = random_prob(name)
    name, which, problem_html = result[0], result[1], result[2]
    if which != None:
      source = 'Source: ' + name + ', ' + which
    else:
      source = 'Source: ' + name

    problem = problem_html
    content = problem.replace('\n', '')

    temp = f"""<body style="background-color: #d4d3cf;"><p><b>{source}</b></p> <br> {content} </body>"""

    html = temp
    image = get_image_from_html(html)

    for i in image:
      with open(i, 'rb') as f:
        picture = discord.File(f)
        await ctx.reply(file=picture)
  except:
    await ctx.reply(
      "Something's wrong. I can feel it. Maybe revise the query to match any of the categories, contests, or subcontests."
    )


@bot.command(description="Fetches a problem matching the given query.")
async def gimme(ctx, *, inputs):
  """Usage: >gimme <name>, <year>, <problem_number>"""
  inputs_list = inputs.split(',')

  inputs_list = [input.strip() for input in inputs_list]

  name = inputs_list[0]
  year = inputs_list[1]
  prob = inputs_list[2]

  problem = give_problem(name, year, prob)
  try:
    content = problem.replace('\n', '')
  except:
    content = "Something's Wrong...I Can Feel It"
  temp = f"""<body style="background-color: #d4d3cf;"> {content} </body>"""

  html = temp
  image = get_image_from_html(html)
  for i in image:
    with open(i, 'rb') as f:
      picture = discord.File(f)
      await ctx.reply(file=picture)


@bot.command(
  description=
  "Fetches the top ranked, unless specified ranking from 1-5, motivation, hints, or complete solution (depends on luck) for the problem matching the given query"
)
async def helpme(ctx, *, inputs):
  """Usage: >helpme <contest>, <year>, <problem_number>, <rank (default=1)> """
  inputs_list = inputs.split(',')

  inputs_list = [input.strip() for input in inputs_list]

  try:
    name = inputs_list[0]
    year = inputs_list[1]
    which = inputs_list[2]
  except:
    name = inputs_list[0]
    year = ''
    which = inputs_list[1]

  try:
    index = inputs_list[3]
  except:
    index = 1
  output = give_solution(name, year, which, index)
  try:
    formatted = ast.literal_eval(output)
    problem = formatted[1]
  except:
    problem = output

  try:
    content = problem.replace('\n', '')
  except:
    content = "Something's Wrong..I Can Feel It"

  temp = f"""<body style="background-color: #d4d3cf;">
      {content}
  </body>"""
  html = temp
  image = get_image_from_html(html)

  for i in image:
    with open(i, 'rb') as f:
      picture = discord.File(f)
      await ctx.send(file=picture)


@bot.command(description="Provides the leaderboard for the Weekly Challenges")
async def leaderboard(ctx):
  """Usage: >leaderboard"""
  leaderboard = get_leaderboard()
  table = tabulate(leaderboard, headers=["UserName", "Score"])
  embed = discord.Embed(title="Weekly Challenges Leaderboard",
                        description=f"```{table}```",
                        color=discord.Color.blue())
  await ctx.channel.send(embed=embed)


@bot.command()
async def ss_leaderboard(ctx):
  data = [('sagarbasyal', 708), ('zraffens', 623), ('vitiate', 431),
          ('yushh0', 300), ('eden', 258), ('theomnipotent69', 100),
          ('johnwick', 100), ('dre7554', 84), ('winzepz', 53), ('aavash', 52),
          ('dewansh', 33)]
  table = tabulate(data, headers=['UserName', 'Final Score'])
  embed = discord.Embed(title='Sunaulo Sanibar Final Standings ',
                        description=f"```{table}```",
                        color=discord.Color.blue())
  await ctx.channel.send(embed=embed)
  await ctx.channel.send(
    'The scores have been standardized with respect to each individual round of games. Pls dm mods if you have any query.'
  )


@bot.command(
  description=
  "Deletes the weekly challenge for specified date. Only available to wc_publisher."
)
@has_role("wc_publisher")
async def del_wc(ctx):
  """Usage: >del_weekly_challenge"""

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel

  await ctx.send(
    'Please enter the date of the weekly challenge you want to remove')
  date = await bot.wait_for("message", check=check)
  date = date.content

  delete_weekly_challenge(date)


@bot.command(
  description=
  'Adds the weekly challenge to be released for specific date. Only available to wc_publisher'
)
@has_role("wc_publisher")
async def set_wc(ctx):
  """Usage: >set_weekly_challenge"""

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel

  await ctx.send("Please upload a image file for the weekly challenge..")
  image_msg = await bot.wait_for("message", check=check)

  if image_msg.attachments:
    attachment = image_msg.attachments[0]
    await ctx.send("Please submit a string as solution.")
    solution_msg = await bot.wait_for("message", check=check)
    solution = solution_msg.content
    await ctx.send(
      "Please enter a date for the challenge of the week (in YYYY-MM-DD format) Or type GG to set the date of coming Saturday"
    )
    date_msg = await bot.wait_for("message", check=check)

    if date_msg.content != 'GG':
      try:
        date = date_msg.content

      except ValueError:
        await ctx.send("Invalid date format")
    else:
      current_date = datetime.datetime.now().date()
      days_ahead = (5 - current_date.weekday() + 7) % 7
      next_saturday = current_date + timedelta(days=days_ahead)
      date = next_saturday

    filename = 'wc/' + str(date) + '_wc_challenge' + '.jpg'

    await attachment.save(filename)

    values = (date, filename, str(solution))
    response = add_weekly_challenge(values)
    await ctx.send(response)
  else:
    await ctx.send("No file uploaded. Please upload a JPG file.")


def get_previous_saturday():
  current_time = datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=5, minutes=45)))
  current_date = current_time.date()

  days_since_saturday = (current_date.weekday() + 1 - 6) % 7

  previous_saturday = current_date - timedelta(days=days_since_saturday)

  return previous_saturday


@bot.command(
  description=
  'Prompts the user to send solution for the current weekly challenge and checks the solution. Use in DM.'
)
async def wc(ctx):
  """Usage: >wc
            >wc <solution>"""

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel

  try:

    previous_saturday = get_previous_saturday()

    file = send_wc(previous_saturday)
    await ctx.send("This Week's Challenge is: ")

    with open(file, 'rb') as f:
      pic = discord.File(f)
      await ctx.send(file=pic)
    await ctx.send("Send the solution without any spaces")

    solution = await bot.wait_for('message', check=check)
    user = solution.author
    print(user)
    print(user.name)
    print('-----')
    solution = solution.content

    correct, response = check_solution(previous_saturday, user.name, solution)
    if correct:
      await ctx.channel.send(
        f"""Congratulations, {ctx.author.mention}! Your solution is correct, and you will get the wc_solver from this Saturday until next Saturday! You can publish your solution in the wc_solution_discussion channel during the time."""
      )

    else:
      await ctx.send(response)
  except:
    await ctx.channel.send(
      'Hmm....Maybe the Weekly Challenge has not been submitted, yet.')


@has_role("wc_publisher")
@bot.command(
  description=
  'Allows wc_publisher to verify a solution of a user and add to leaderboard')
async def gg(ctx, *user):
  user = ' '.join(user)
  guild_id = 1044240356943876186
  guild = bot.get_guild(guild_id)

  update_leaderboard(user)

  for guild_member in guild.members:
    if guild_member.name == user:
      member = guild_member
      break

  if member is not None:
    add_to_wc_solvers(user)
    await ctx.send(f'Updated leaderboard for {user}')
  else:
    await ctx.send(f'User "{user}" not found.')


async def remove_wc_solver():
  guild_id = 1044240356943876186
  guild = bot.get_guild(guild_id)
  role_name = "wc_solver"
  role = discord.utils.get(guild.roles, name=role_name)
  for member in guild.members:
    if role in member.roles:
      await member.remove_roles(role)

  channel_id = 1110417376815620177
  channel = bot.get_channel(channel_id)
  #await channel.send(f"The {role_name} role has been removed from all role holders.")


"""async def add_wc_solver(member_list):
  role_name = 'wc_solver'
  guild_id = 1044240356943876186
  channel_id = 1110417376815620177
  guild = bot.get_guild(guild_id)
  channel = bot.get_channel(channel_id)

  wc_solver_role = discord.utils.get(guild.roles, name=role_name)
  for member_id in member_list:
    
    member = guild.get_member(member_id)
    if member is not None:
      await member.add_roles(wc_solver_role)
      await channel.send(f'wc_role given to {member}')
    else:
      await channel.send('No solvers for the last week challenge.')
  remove_all_from_wc_solvers()"""


async def add_wc_solver(member_list):
  role_name = 'wc_solver'
  guild_id = 1044240356943876186
  channel_id = 1110417376815620177
  guild = bot.get_guild(guild_id)
  channel = bot.get_channel(channel_id)
  wc_solver_role = discord.utils.get(guild.roles, name=role_name)
  for username in member_list:
    member = None
    for guild_member in guild.members:
      if guild_member.name == username:
        member = guild_member
        break

    if member is not None:
      await member.add_roles(wc_solver_role)
      await channel.send(f'wc_role given to {member}')
    else:
      await channel.send(f'User "{username}" not found.')
  remove_all_from_wc_solvers()


async def publish_wc():
  channel_id = 1044942923311087646
  channel = bot.get_channel(channel_id)
  date = get_previous_saturday()
  try:
    file = send_wc(date)
    with open(file, 'rb') as f:
      picture = discord.File(f)
      await channel.send(
        """Hey @everyone! The challenge for this week has been published""")
      await channel.send(file=picture)
  except:
    print('No wc found...')


async def every_saturday():
  await bot.wait_until_ready()
  while not bot.is_closed():
    now_nepal = datetime.datetime.now(nepal_timezone)
    if now_nepal.weekday(
    ) == 5 and now_nepal.hour == 0 and now_nepal.minute == 1 and now_nepal.second == 0:
      try:
        print('removing wc solver')
        await remove_wc_solver()
      except:
        None
      try:
        print('publishing wc')
        await publish_wc()
      except:
        None
      try:
        print('adding wc_solver')
        previous_solvers = get_all_wc_solvers()
        await add_wc_solver(previous_solvers)
      except:
        None

    await asyncio.sleep(1)


@bot.event
async def on_ready():
  online_text = '{0.user} is online. I seek commands.'.format(bot)
  print(online_text)

  bot.loop.create_task(every_saturday())


stay_awake()
bot.run(token)
