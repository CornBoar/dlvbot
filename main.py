import discord
from discord import app_commands
import json
import random
import string
import pointercratepy
import gd
import geometrydash as gda
import requests
from bs4 import BeautifulSoup
import typing

gd = gd.Client()

xp_to_level = {300: 1, 600: 2, 900: 3, 1400: 4, 1900: 5, 2650: 6, 3400: 7, 4150: 8, 4900: 9, 5650: 10, 7150: 11, 8650: 12, 10150: 13, 11650: 14, 13150: 15, 15150:
               16, 17150: 17, 19150: 18, 21150: 19, 23150: 20, 26150: 21, 29150: 22, 32150: 23, 35150: 24, 38150: 25, 41150: 26, 44150: 27, 47150: 28, 50150: 29,
               53150: 30, 58150: 31, 63150: 32, 68150: 33, 73150: 34, 78150: 35, 83150: 36, 88150: 37, 93150: 38, 98150: 39, 103150: 40, 110650: 41, 118150: 42,
               125650: 43, 133150: 44, 140650: 45, 148150: 46, 155650: 47, 163150: 48, 170650: 49, 178150: 50}

def xp_to_lvl(xp_amount: int) -> tuple:
    if xp_amount > 188149:
        add = xp_amount - 188450
        add_remainder = add % 10000
        add = add // 10000
        return 50 + add, add_remainder
    for i in reversed(xp_to_level):
        if xp_amount >= i:
            level = xp_to_level[i]
            remainder = xp_amount - i
            return level, remainder

with open(r'C:\Users\Dani1\DLVBOTXPSAVES.json', 'r') as f:
    saves = json.load(f)

with open(r'C:\Users\Dani1\DLVLIST.json', 'r') as f:
    dlv_list = json.load(f)

with open(r'C:\Users\Dani1\DLVUSERS.json', 'r') as f:
    dlv_users = json.load(f)

with open(r'C:\Users\Dani1\DLVKEYS.json', 'r') as f:
    dlv_keys = json.load(f)

with open(r'C:\Users\Dani1\DLVCOMPLETIONDATES.json', 'r') as f:
    dlv_completion_dates = json.load(f)

with open(r'C:\Users\Dani1\DLVTHINGY.json', 'r') as f:
    dlv_thingy = json.load(f)

def save():
    json.dump(saves, open(r'C:\Users\Dani1\DLVBOTXPSAVES.json', 'w'))
    json.dump(dlv_list, open(r'C:\Users\Dani1\DLVLIST.json', 'w'))
    json.dump(dlv_users, open(r'C:\Users\Dani1\DLVUSERS.json', 'w'))
    json.dump(dlv_keys, open(r'C:\Users\Dani1\DLVKEYS.json', 'w'))
    json.dump(dlv_completion_dates, open(r'C:\Users\Dani1\DLVCOMPLETIONDATES.json', 'w'))
    json.dump(dlv_thingy, open(r'C:\Users\Dani1\DLVTHINGY.json', 'w'))

def get_user_id(username):
    for i, e in list(dlv_users.items()):
        if e['username'] == username:
            return i
    return None

def hex_to_rgb(hex_code):
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client=client)

@tree.command(name='addxp', description='Add XP to a user. Can only be used by Dr. Slug.')
async def add_xp(interaction: discord.Interaction, amount: int, user: discord.Member):
    if not saves.__contains__(str(interaction.user.id)):
        saves[str(interaction.user.id)] = {'xp': 0, 'username': interaction.user.name, 'avatar': str(client.get_user(int(interaction.user.id)).avatar), 'user_id': str(interaction.user.id)}
        save()
    if str(interaction.user.id) == '543885678258290699':
        if saves.__contains__(str(user.id)):
            saves[str(user.id)]['xp'] += amount
            save()
            await interaction.response.send_message(embed=discord.Embed(title=f'Successfully added {amount} XP to {user.name}. They now have {saves[str(user.id)]["xp"]} XP and are level {saves[str(user.id)]["xp"] // 1000}.',
                                                                        colour=discord.Colour.green()))
        else:
            saves[str(user.id)] = {'xp': amount, 'username': user.name}
            save()
            await interaction.response.send_message(embed=discord.Embed(title=f'Successfully added {amount} XP to {user.name}. They now have {saves[str(user.id)]["xp"]} XP and are level {saves[str(user.id)]["xp"] // 1000}.',
                                                                        colour=discord.Colour.green()))
    else:
        await interaction.response.send_message(embed=discord.Embed(title='You are not Dr. Slug!', colour=discord.Colour.red()), ephemeral=True)

@tree.command(name='takexp', description='Take XP from a user. Can only be used by Dr. Slug.')
async def take_xp(interaction: discord.Interaction, amount: int, user: discord.Member):
    if not saves.__contains__(str(interaction.user.id)):
        saves[str(interaction.user.id)] = {'xp': 0, 'username': interaction.user.name, 'avatar': str(client.get_user(int(interaction.user.id)).avatar), 'user_id': str(interaction.user.id)}
        save()
    if str(interaction.user.id) == '543885678258290699':
        if saves.__contains__(str(user.id)):
            saves[str(user.id)]['xp'] -= amount
            if saves[str(user.id)]['xp'] < 0:
                saves[str(user.id)]['xp'] = 0
            save()
            await interaction.response.send_message(embed=discord.Embed(title=f'Successfully took {amount} XP from {user.name}. They now have {saves[str(user.id)]["xp"]} XP and are level {saves[str(user.id)]["xp"] // 1000}.',
                                                                        colour=discord.Colour.green()))
        else:
            saves[str(user.id)] = {'xp': 0, 'username': user.name, 'user_id': str(user.id)}
            save()
            await interaction.response.send_message(embed=discord.Embed(title=f'Successfully took {amount} XP from {user.name}. They now have {saves[str(user.id)]["xp"]} XP and are level {saves[str(user.id)]["xp"] // 1000}.',
                                                                        colour=discord.Colour.green()))
    else:
        await interaction.response.send_message(embed=discord.Embed(title='You are not Dr. Slug!', colour=discord.Colour.red()), ephemeral=True)

@tree.command(name='xp', description='Check yours or someone elses XP.')
async def xp(interaction: discord.Interaction, user: discord.Member=None):
    if not saves.__contains__(str(interaction.user.id)):
        saves[str(interaction.user.id)] = {'xp': 0, 'username': interaction.user.name, 'avatar': str(client.get_user(int(interaction.user.id)).avatar), 'user_id': str(interaction.user.id)}
        save()
    if user is None:
        user = interaction.user
    if saves.__contains__(str(user.id)):
        await interaction.response.send_message(embed=discord.Embed(title=f'{user.name}', description=f'**XP:** {saves[str(user.id)]["xp"]}\n**LEVEL:** {saves[str(user.id)]["xp"] // 1000}', colour=discord.Colour.blurple()))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=f'**XP:** 0\n**LEVEL:** 0', colour=discord.Colour.blurple()))

@tree.command(name='leaderboard', description='View the top 10 users.')
async def leaderboard(interaction: discord.Interaction):
    class LeaderboardButtons(discord.ui.View):
        @discord.ui.button(label='Show More/Less', style=discord.ButtonStyle.blurple)
        async def show_more_button(self, button_press: discord.Interaction, button: discord.ui.Button):
            if button_press.message.embeds[0].description.__contains__('**11.**'):
                if not saves.__contains__(str(interaction.user.id)):
                    saves[str(interaction.user.id)] = {'xp': 0, 'username': interaction.user.name, 'avatar': str(client.get_user(int(interaction.user.id)).avatar), 'user_id': str(interaction.user.id)}
                    save()
                sorted_saves = list(sorted(saves.items(), key=lambda x: x[1]['xp'], reverse=True))
                lb = ''
                for i in sorted_saves[:10]:
                    lb += f'**{sorted_saves.index(i) + 1}.** ' + i[1]['username'] + f': {saves[i[0]]["xp"]} XP, Level {saves[i[0]]["xp"] // 1000}\n'
                await button_press.message.edit(embed=discord.Embed(title='Top 10 Users:', description=lb, colour=discord.Colour.blurple()), view=LeaderboardButtons())
                await button_press.response.send_message(' ', ephemeral=True)
            else:
                if not saves.__contains__(str(interaction.user.id)):
                    saves[str(interaction.user.id)] = {'xp': 0, 'username': interaction.user.name, 'avatar': str(client.get_user(int(interaction.user.id)).avatar), 'user_id': str(interaction.user.id)}
                    save()
                sorted_saves = list(sorted(saves.items(), key=lambda x: x[1]['xp'], reverse=True))
                lb = ''
                for i in sorted_saves[:100]:
                    lb += f'**{sorted_saves.index(i) + 1}.** ' + i[1]['username'] + f': {saves[i[0]]["xp"]} XP, Level {saves[i[0]]["xp"] // 1000}\n'
                await button_press.message.edit(embed=discord.Embed(title='Top 100 Users:', description=lb, colour=discord.Colour.blurple()))
                await button_press.response.send_message(' ', ephemeral=True)
    if not saves.__contains__(str(interaction.user.id)):
        saves[str(interaction.user.id)] = {'xp': 0, 'username': interaction.user.name, 'avatar': str(client.get_user(int(interaction.user.id)).avatar), 'user_id': str(interaction.user.id)}
        save()
    sorted_saves = list(sorted(saves.items(), key=lambda x: x[1]['xp'], reverse=True))
    lb = ''
    for i in sorted_saves[:10]:
        lb += f'**{sorted_saves.index(i) + 1}.** ' + i[1]['username'] + f': {saves[i[0]]["xp"]} XP, Level {saves[i[0]]["xp"] // 1000}\n'
    await interaction.response.send_message(embed=discord.Embed(title='Top 10 Users:', description=lb, colour=discord.Colour.blurple()), view=LeaderboardButtons())

@tree.command(name='generatekey', description='Generate a key for the admin website. Can only be used by Dr. Slug.')
async def generate_key(interaction: discord.Interaction):
    if str(interaction.user.id) in ['543885678258290699', '991443322516279466']:
        dlv_keys['main'] = ''
        for i in range(10):
            dlv_keys['main'] += random.choice(string.ascii_letters + '12345678910')
        save()
        await interaction.response.send_message(embed=discord.Embed(title=f'Your Key Is: {dlv_keys["main"]}', description='This key will be valid until you generate a new one.', colour=discord.Colour.green()), ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(title=f'You Are Not Dr. Slug!', colour=discord.Colour.red()), ephemeral=True)

@client.event
async def on_message(message):
    global dlv_users
    if str(message.guild.id) == '1113413337410175088':
        roles = list(message.guild.roles)
        roles.pop(0)
        # print(roles)
        if dlv_list == {} or 1 == 1:
            dlv_list['main'] = []
            dlv_list['colors'] = {}
            dlv_list['victors'] = {}
            dlv_list['positions'] = {}
            dlv_list['gd_stats'] = {}
        demons = pointercratepy.Client.get_demons(limit=100) + pointercratepy.Client.get_demons(limit=100, after=100) + pointercratepy.Client.get_demons(limit=100, after=200) + pointercratepy.Client.get_demons(limit=100, after=300) \
        + pointercratepy.Client.get_demons(limit=100, after=400)
        demons_dict = {}
        # print(roles)
        for i in demons:
            demons_dict[i['name'].lower()] = int(i['position'])
        for i in roles:
            if i.name not in ['@everyone', 'ingore this role', 'admin']:
                # if i.name.title() not in dlv_list['main']:
                victors = []
                for e in list(dlv_users.values()):
                    if e['completions'].__contains__(i.name.title()):
                        victors.append(e['username'])
                dlv_list['main'].append(i.name.title())
                dlv_list['colors'][i.name.title()] = str(i.color)
                dlv_list['victors'][i.name.title()] = victors
                try:
                    assert 1 == 2
                except Exception as error:
                    print(str(error).strip(str(error)))
                    class lvl:
                        def __init__(self):
                            class creator:
                                def __init__(self):
                                    self.name = 'Error'
                                    self.account_id = 'Error'
                            class song:
                                def __init__(self):
                                    self.name = 'Error'
                            self.creator = creator()
                            self.difficulty = 'Error'
                            self.downloads = 0
                            self.rating = 0
                            self.length = 'Error'
                            self.object_count = 0
                            self.game_version = 'Error'
                            self.song = song()
                            self.id = 'Error'
                    lvl = lvl()
            try:
                author = lvl.creator.name
            except AttributeError:
                author = '-'
            author_id = lvl.creator.account_id
            gd_stats = {'uploaded_by': author, 'author_id': author_id, 'difficulty': lvl.difficulty, 'downloads': f'{lvl.downloads:,}',
                        'likes': f'{lvl.rating:,}', 'length': lvl.length, 'object_count': f'{lvl.object_count:,}', 'last_updated_in_version': lvl.game_version, 'song': lvl.song.name, 'level_id': lvl.id}
            dlv_list['gd_stats'][i.name.title()] = gd_stats
            try:
                dlv_list['positions'][i.name.title()] = demons_dict[i.name.lower()]
            except KeyError:
                dlv_list['positions'][i.name.title()] = 'Not On Any Pointercrate List'
        users = list(message.guild.members)
        dlv_users = {}
        for i in users:
            if not saves.__contains__(str(i.id)):
                saves[str(i.id)] = {'xp': 0, 'username': i.name, 'avatar': str(client.get_user(int(i.id)).avatar), 'user_id': str(i.id)}
            user_completions = []
            for e in i.roles:
                if e.name not in ['@everyone', 'ingore this role', 'admin']:
                    user_completions.append(e.name.title())
            dlv_users[str(i.id)] = {'completions': user_completions, 'username': str(i.name), 'avatar': str(client.get_user(int(i.id)).avatar), 'user_id': str(i.id)}
            if not str(i.id) in list(dlv_completion_dates.keys()):
                dlv_completion_dates[str(i.id)] = {i: None for i in user_completions}
        save()

@tree.command(name='victors', description="View a demon's victors")
async def victors_command(interaction: discord.Interaction, demon: str):
    awesome_dict_i_literally_came = {i: (dlv_completion_dates[get_user_id(i)][demon] if dlv_completion_dates[get_user_id(i)][demon] else '100000000000.1.1') for i in set(dlv_list['victors'][demon])}
    sorted_dates = sorted(list(awesome_dict_i_literally_came.items()), key=lambda x: tuple(map(int, x[1].split('.'))))
    formatted_victors = ''
    thingy = 0
    for i in sorted_dates:
        if thingy == 0:
            formatted_victors += '**VERIFIER:**\n' + i[0] + '\n'
        elif thingy == 1:
            formatted_victors += '**FIRST VICTOR:**\n' + i[0] + '\n'
        else:
            formatted_victors += i[0] + '\n'
        thingy += 1
    formatted_victors.replace('\n', ' (Verifier)‎\n', 1)
    formatted_victors.replace('\n', ' (First Victor)‎\n', 1)
    await interaction.response.send_message(embed=discord.Embed(title=f'Victors Of {demon}', description=formatted_victors, colour=discord.Colour.from_rgb(*hex_to_rgb(dlv_list['colors'][demon].strip('#')))))

months = ['1 - January', '2 - February', '3 - March', '4 - April', '5 - May', '6 - June', '7 - July', '8 - August', '9 - September', '10 - October', '11 - November', '12 - December']

@tree.command(name='addcompletion', description='Add a completion to a user. (Can Only Be Used By Dr. Slug)')
async def add_completion_command(interaction: discord.Interaction, user: discord.Member, demon: str, year: int, month: typing.Literal[*months], day: int):
    if str(interaction.user.id) in ['543885678258290699', '991443322516279466']:
        dlv_thingy['main'] = True
        if day > 31:
            await interaction.response.send_message(embed=discord.Embed(title='Day Cannot Be Higher Than 31.', colour=discord.Colour.red()), ephemeral=True)
        users = list(interaction.guild.members)
        for i in users:
            if not saves.__contains__(str(i.id)):
                saves[str(i.id)] = {'xp': 0, 'username': i.name, 'avatar': str(client.get_user(int(i.id)).avatar), 'user_id': str(i.id)}
            user_completions = []
            for e in i.roles:
                if e.name not in ['@everyone', 'ingore this role', 'admin']:
                    user_completions.append(e.name.title())
            dlv_users[str(i.id)] = {'completions': user_completions, 'username': str(i.name), 'avatar': str(client.get_user(int(i.id)).avatar), 'user_id': str(i.id)}
            if not str(i.id) in list(dlv_completion_dates.keys()):
                dlv_completion_dates[str(i.id)] = {i: None for i in user_completions}
            dlv_completion_dates[str(user.id)][demon] = f'{year}.{months.index(month) + 1}.{day}'
            print(dlv_users)
            if dlv_thingy['main']:
                await interaction.channel.send(embed=discord.Embed(title=f"Successfully Added {demon} To {user.name}'s Completions (Completed On {year}.{months.index(month) + 1}.{day})!", colour=discord.Colour.green()))
                dlv_thingy['main'] = False
        role = ''
        for j in interaction.guild.roles:
            if j.name == demon.lower():
                role = j
                break
        await user.add_roles(role)
        dlv_users[str(user.id)]['completions'].append(str(role.name.title()))
        dlv_list['victors'][demon.title()].append(str(user.name))
        await on_message(await client.get_channel(1113413337410175090).fetch_message(1138617022138290176))
    else:
        await interaction.response.send_message(embed=discord.Embed(title='You Are Not Dr. Slug!', colour=discord.Colour.red()), ephemeral=True)

@tree.command(name='removecompletion', description='Remove a completion from a user. (Can Only Be Used By Dr. Slug)')
async def remove_completion_command(interaction: discord.Interaction, user: discord.Member, demon: str):
    dlv_thingy['main2'] = True
    if str(interaction.user.id) in ['543885678258290699', '991443322516279466']:
        print(dlv_users)
        if dlv_users[str(user.id)]['completions'].__contains__(demon):
            if str(interaction.user.id) in ['543885678258290699', '991443322516279466']:
                users = list(interaction.guild.members)
                for i in users:
                    if not saves.__contains__(str(i.id)):
                        saves[str(i.id)] = {'xp': 0, 'username': i.name, 'avatar': str(client.get_user(int(i.id)).avatar), 'user_id': str(i.id)}
                    user_completions = []
                    for e in i.roles:
                        if e.name not in ['@everyone', 'ingore this role', 'admin']:
                            user_completions.append(e.name.title())
                    dlv_users[str(i.id)] = {'completions': user_completions, 'username': str(i.name), 'avatar': str(client.get_user(int(i.id)).avatar), 'user_id': str(i.id)}
                    if not str(i.id) in list(dlv_completion_dates.keys()):
                        dlv_completion_dates[str(i.id)] = {i: None for i in user_completions}
                    new_list = []
                    for i in dlv_users[str(user.id)]['completions']:
                        if i != demon.title():
                            new_list.append(i)
                    new_list2 = []
                    for i in dlv_list['victors'][demon.title()]:
                        if i != str(user.name):
                            new_list2.append(str(user.name))
                    dlv_users[str(user.id)]['completions'] = new_list
                    dlv_list['victors'][demon.title()] = new_list2
                    if dlv_thingy['main2']:
                        await interaction.channel.send(embed=discord.Embed(title=f"Successfully Removed {demon} From {user.name}'s Completions.", colour=discord.Colour.red()))
                        dlv_thingy['main2'] = False
                role = ''
                for j in interaction.guild.roles:
                    if j.name == demon.lower():
                        role = j
                        break
                await user.remove_roles(role)
                await on_message(await client.get_channel(1113413337410175090).fetch_message(1138617022138290176))
        else:
            await interaction.response.send_message(embed=discord.Embed(title='That User Has Not Completed That Demon.', colour=discord.Colour.red()), ephemeral=True)
    else:
        await interaction.response.send_message(embed=discord.Embed(title='You Are Not Dr. Slug!', colour=discord.Colour.red()), ephemeral=True)

@tree.command(name='demonlist', description='Display the Demon List.')
async def demon_list_command(interaction: discord.Interaction):
    formatted_list = ''
    for i in interaction.guild.roles[::-1]:
        if i.name not in ['@everyone', 'ingore this role', 'admin']:
            formatted_list += f'**{interaction.guild.roles[::-1].index(i) - 1}**. <@&{i.id}>\n'
    await interaction.response.send_message(embed=discord.Embed(title='Demon List', description=formatted_list, colour=discord.Colour.from_rgb(*hex_to_rgb(dlv_list['colors'][dlv_list['main'][::-1][0]].strip('#')))))

@client.event
async def on_ready():
    await tree.sync()
    print('Ready!')

client.run('TOKEN')
