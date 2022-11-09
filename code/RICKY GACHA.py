import os
from discord.ext import commands
from datetime import datetime, timedelta
#from replit import db
import discord
from discord import Color
import random
#import requests
#from flask import Flask, render_template
#from threading import Thread
import asyncio
#import replit
import copy
import math
from dotenv import load_dotenv

#bot setup
load_dotenv()
#APP_ID = os.environ['APP-ID']
#APP_SECRET = os.environ['APP-SECRET']
TOKEN = os.environ['TOKEN']
my_bot = commands.Bot(command_prefix="ricky ")

#reddit token setup
#REDDIT_USERNAME = os.environ['REDDIT-USERNAME']
#REDDIT_PASSWORD = os.environ['REDDIT-PASS']
#REDDIT_URL = 'https://www.reddit.com/'
#API_URL = 'https://oauth.reddit.com'
limit = 100
current_time = datetime.now()
refresh_time = datetime.now()

#Cache and optimization
CACHE = {}
CURRENT_RAIDS = {
}  #raids are not persistent and will cease after server restart; this is ok since raids are quick.


#def refresh_token():
#    data = {
#        'grant_type': 'password',
#        'username': REDDIT_USERNAME,
#        'password': REDDIT_PASSWORD
#    }
#    auth = requests.auth.HTTPBasicAuth(APP_ID, APP_SECRET)
#    r = requests.post(
#        REDDIT_URL + 'api/v1/access_token',
#        data=data,
#        headers={'User-Agent': 'ricky-simulator by u/BetaThunder'},
#        auth=auth)
#    d = r.json()
#    return 'bearer ' + d['access_token']
    #


async def save():
    global CACHE
    print("Saving cache ! Don't do anything bad .")
    with open("USER_DATA.gachasavedata", "w") as savefile:
        savefile.write(str(CACHE))
    #for u in CACHE:
        #db[u] = copy.deepcopy(replit.database.to_primitive(CACHE[u]))
        #print("New database entry ", db[u], id(db[u]), id(CACHE[u]))

    print(f"saved at {datetime.now()}", len(CACHE), "keys to the database.")


@my_bot.command("GIVE_ONE_THOUSAND_WISHES")
async def admin_onek_wishes(message):
    if str(message.author.id) == "328039243303616523":
        user_id = message.message.content.split(" ")[2]
        #user_data =
        #user_data = {}
        if user_id not in CACHE:
        #    if user_id not in db.keys():
        #        db[user_id] = {}
            CACHE[user_id] = {}
        user_data = CACHE[user_id]
        #if user_id not in CACHE:
        #    CACHE[user_id] = copy.copy(
        #        replit.database.to_primitive(db[user_id]))
        #user_data = copy.copy(replit.database.to_primitive(CACHE[user_id]))
        print(user_id, "wish granted")
        user_data["gachaCooldown"] = (
            datetime.now() -
            timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")
        CACHE[user_id] = user_data


@my_bot.command("ADMIN_SAVE")
async def admin_save_all(message):
    if str(message.author.id) == "328039243303616523":
        print("Admin requested saving...")
        await save()


async def autosave():
    while True:
        await save()
        await asyncio.sleep(300)


class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.EASY_ITEM_NAMES = {}
        self.THREE_STAR_DATA = {}
        self.FOUR_STAR_DATA = {}
        self.FIVE_STAR_DATA = {}
        self.SIX_STAR_DATA = {}
        self.ALL_STAR_DATA = {}
        self.SKIN_DATA = {}
        self.STATS = {}
        self.BEST_PULL_RATINGS = {
            "MIN": -99999,
            "3": 1,
            "4": 2,
            "5": 3,
            "Special": 4,
            "Exquisite": 5,
            "Exclusive": 6
        }
        self.HIGHLIGHT_COLORS = {
            "3": Color.blue(),
            "4": Color.purple(),
            "5": Color.gold(),
            "Special": Color.red(),
            "Exquisite": Color.magenta(),
            "Exclusive": Color.dark_gold(),
            "6": Color.dark_gold()
        }
        self.STAR_NUMBER_CONVERSION = {
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "Special": 4,
            "Exquisite": 5,
            "Exclusive": 6
        }
        self.get_pulls()
        self.get_skins()
        self.get_stats()

    def get_stats(self):
        stats_file = open("STATS.txt", "r")
        all_stats_info = stats_file.read()
        stats_data = all_stats_info.split("\n")
        for i in stats_data:
            if len(i) > 0:
                current_item = i.split(";;")
                #print(current_item)
                #break
                self.STATS[current_item[0]] = {
                    "health": int(current_item[1]),
                    "attack": int(current_item[2]),
                    "defence": int(current_item[3]),
                    "speed": int(current_item[4])
                }
        stats_file.close()

    def get_pulls(self):
        pulls_file = open("PULLS.txt", "r", encoding='utf8')
        all_pulls_info = pulls_file.read()
        pulls_data = all_pulls_info.split("-STAR UP-")
        THREE_STARS = pulls_data[0].split("\n")
        FOUR_STARS = pulls_data[1].split("\n")
        FIVE_STARS = pulls_data[2].split("\n")
        SIX_STARS = pulls_data[3].split("\n")
        self.THREE_STAR_DATA = {}
        self.FOUR_STAR_DATA = {}
        self.FIVE_STAR_DATA = {}
        self.SIX_STAR_DATA = {}
        for x in THREE_STARS:
            if len(x) > 0:
                item_info = x.split("[]")
                self.THREE_STAR_DATA[item_info[0]] = item_info[1:]
                self.EASY_ITEM_NAMES[item_info[0].lower()] = item_info[0]
        for x in FOUR_STARS:
            if len(x) > 0:
                item_info = x.split("[]")
                self.FOUR_STAR_DATA[item_info[0]] = item_info[1:]
                self.EASY_ITEM_NAMES[item_info[0].lower()] = item_info[0]
        for x in FIVE_STARS:
            if len(x) > 0:
                item_info = x.split("[]")
                self.FIVE_STAR_DATA[item_info[0]] = item_info[1:]
                self.EASY_ITEM_NAMES[item_info[0].lower()] = item_info[0]
        for x in SIX_STARS:
            if len(x) > 0:
                item_info = x.split("[]")
                self.SIX_STAR_DATA[item_info[0]] = item_info[1:]
                self.EASY_ITEM_NAMES[item_info[0].lower()] = item_info[0]
        self.ALL_STAR_DATA = {
            "3": self.THREE_STAR_DATA,
            "4": self.FOUR_STAR_DATA,
            "5": self.FIVE_STAR_DATA,
            "6": self.SIX_STAR_DATA
        }
        pulls_file.close()

    def skin_to_item_if_possible(self, skin_request):
        selected_item = skin_request
        skin_converted = False
        for item in self.SKIN_DATA:
            for skin in self.SKIN_DATA[item]:
                if skin[1].lower() in skin_request.lower():
                    selected_item = item
                    skin_converted = True
                    skin_request = skin[1]
                    #selected_skin = skin[1]
                    break
        return selected_item, skin_converted, skin_request

    def get_star_value(self, item):
        if item in self.THREE_STAR_DATA:
            return "3"
        elif item in self.FOUR_STAR_DATA:
            return "4"
        elif item in self.FIVE_STAR_DATA:
            return "5"
        elif item in self.SIX_STAR_DATA:
            return "Exclusive"
        else:
            return None

    def get_skins(self):
        skins_file = open("SKINS.txt", "r")
        all_skins_info = skins_file.read()
        ALL_SKINS = all_skins_info.split("\n")
        self.SKIN_DATA = {}
        for s in ALL_SKINS:
            if len(s) > 0:
                item_info = s.split("[]")
                if item_info[0] not in self.SKIN_DATA:
                    self.SKIN_DATA[item_info[0]] = []
                self.SKIN_DATA[item_info[0]].append(item_info[1:])
        skins_file.close()

    def select_item(self, since_4: int, since_5: int, user_data: dict):
        selected_item = ""
        star_quality = 0
        dice = random.uniform(0, 1)
        #print(str(0.1 + since_4 / 20))
        if dice < 0.01 + since_5 / 5000:
            star_quality = "5"
        elif dice < 0.1 + since_4 / 20:
            star_quality = "4"
        else:
            star_quality = "3"
        selected_item = random.choice(list(self.ALL_STAR_DATA[star_quality]))

        selected_skin = None
        skin_dice = random.uniform(0, 1)
        if skin_dice < 0.02:
            if selected_item in self.SKIN_DATA:
                attempts = 25
                selected_skin = random.choice(self.SKIN_DATA[selected_item])
                while attempts > 0 and "skinLoot" in user_data and selected_item in user_data[
                        "skinLoot"] and selected_skin[1] in user_data[
                            "skinLoot"][selected_item]:
                    selected_skin = random.choice(
                        self.SKIN_DATA[selected_item])
                    attempts -= 1
                if star_quality == "4":
                    star_quality = "Special"
                elif star_quality == "5":
                    star_quality = "Exquisite"
        return selected_item, star_quality, selected_skin

    def get_data(self, author: discord.Member):
        global CACHE
        user_data = {}
        user_id = str(author.id)
            #CACHE[user_id] = {}
        if user_id not in CACHE:
            CACHE[user_id] = {}
            #CACHE[user_id] = {}
            #CACHE[user_id] = copy.copy(
            #    replit.database.to_primitive(db[user_id]))
        user_data = CACHE[user_id]
        #print(user_data == CACHE[user_id])
        #print(CACHE[user_id] == db[user_id])
        #print(user_data == db[user_id])
        return user_data

    def change_equipped_skin(self, user_data, selected_item, selected_skin):
        success_status = -1
        if "skinLoot" not in user_data:
            user_data["skinLoot"] = {}
        skin_loot = user_data["skinLoot"]
        if selected_item not in skin_loot or selected_skin not in skin_loot[
                selected_item]:
            #await ctx.send(f"{ctx.author.mention}, you don't have that skin!")
            success_status = -1
        else:
            current_selection = skin_loot[selected_item][selected_skin]
            for skin in self.SKIN_DATA[selected_item]:
                if skin[1] in skin_loot[selected_item]:
                    skin_loot[selected_item][skin[1]] = False
            if current_selection:
                skin_loot[selected_item][selected_skin] = False
                #await ctx.send(f"{ctx.author.mention}, **{selected_skin}** for **{selected_item}** has been **unequipped!**")
                success_status = 0
            else:
                skin_loot[selected_item][selected_skin] = True
                success_status = 1
                #await ctx.send(f"{ctx.author.mention}, **{selected_skin}** for **{selected_item}** has been **selected!**")
        user_data["skinLoot"] = skin_loot
        return user_data, success_status

    def create_gacha_embed(self, item: str, skin, star_quality: str, author,
                           other_items):
        embed_title = ""
        if skin == None:
            embed_title = f"{author}'s {item} ({star_quality}:star2:)"
        else:
            embed_title = f"{author}'s {skin[1]} ({star_quality}:star2:)"
        embed_description = f"*{self.ALL_STAR_DATA[str(self.STAR_NUMBER_CONVERSION[star_quality])][item][2]}*"
        embed_color = self.HIGHLIGHT_COLORS[star_quality]
        embed_footer = f"From {self.ALL_STAR_DATA[str(self.STAR_NUMBER_CONVERSION[star_quality])][item][1]}"
        current_embed = discord.Embed(title=embed_title,
                                      description=embed_description,
                                      color=embed_color)
        if skin == None:
            current_embed.set_image(url=self.ALL_STAR_DATA[str(
                self.STAR_NUMBER_CONVERSION[star_quality])][item][0])
        else:
            current_embed.set_image(url=skin[0])
            embed_footer += f" ({skin[2]})"

        for i in other_items:
            current_embed.add_field(name=i,
                                    value=f"x{other_items[i]}",
                                    inline=True)
        current_embed.set_footer(text=embed_footer)
        #print("Embed", embed_title, embed_description,  embed_footer, self.ALL_STAR_DATA[str(self.STAR_NUMBER_CONVERSION[star_quality])][item][0])
        return current_embed

    @commands.command()
    async def flex(self, ctx):
        user_data = self.get_data(ctx.author)

        user_request = ctx.message.content.split(" ")
        if len(user_request
               ) == 3 and user_request[2] in self.STAR_NUMBER_CONVERSION:
            #print("w")
            if user_request[2] == "Special" or user_request[2] == "Exquisite":
                if "skinLoot" not in user_data:
                    await ctx.send(
                        f"{ctx.author.mention}, we don't have any data for you."
                    )
                    return
                my_embed = discord.Embed(
                    title=f"{ctx.author}'s {user_request[2]}:star2: Skins",
                    description=f"*{ctx.author} owns the following:*\n\n",
                    color=self.HIGHLIGHT_COLORS[user_request[2]])
                my_embed.set_thumbnail(url=ctx.author.avatar_url_as(
                    format="png"))
                for i in user_data["skinLoot"]:
                    if i in self.ALL_STAR_DATA[str(
                            self.STAR_NUMBER_CONVERSION[user_request[2]])]:
                        for j in user_data["skinLoot"][i]:
                            my_embed.add_field(
                                name=j,
                                value="*Equipped: " +
                                str(user_data["skinLoot"][i][j]) + "*",
                                inline=True)
                await ctx.send(embed=my_embed)
            else:
                if "gachaLoot" not in user_data:
                    await ctx.send(
                        f"{ctx.author.mention}, we don't have any data for you."
                    )
                    return
                user_star_request = str(
                    self.STAR_NUMBER_CONVERSION[user_request[2]])
                my_embed = discord.Embed(
                    title=f"{ctx.author}'s {user_star_request}:star2: Items",
                    description=f"*{ctx.author} owns the following:*\n\n",
                    color=self.HIGHLIGHT_COLORS[user_star_request])
                my_embed.set_thumbnail(url=ctx.author.avatar_url_as(
                    format="png"))
                for i in user_data["gachaLoot"]:
                    if i in self.ALL_STAR_DATA[str(
                            self.STAR_NUMBER_CONVERSION[user_request[2]])]:
                        my_embed.add_field(
                            name=i,
                            value="*x" + str(user_data["gachaLoot"][i]) + "*",
                            inline=True)
                await ctx.send(embed=my_embed)
        else:
            await ctx.send(
                f"{ctx.author.mention}, invalid request! Example usage: `ricky flex 3`, `ricky flex Special`."
            )
            return

    #a note on levelling: 3 stars: 20x dupes (lvl 20) = 2x stronger, so 4x dupes for four stars = 2x stronger, and 0.8x for 5 stars

    @commands.command()
    async def raidboss(self, ctx):
        def check(message: discord.Message):
            return message.channel == ctx.channel and not message.author.bot and str(
                message.author.id) in CURRENT_RAIDS[guild]["participants"]

        global CACHE, CURRENT_RAIDS
        user_data = self.get_data(ctx.author)
        user_id = str(ctx.author.id)

        #if user_id != "328039243303616523":
        #await ctx.send(f"{ctx.author.mention}, this command is currently incomplete (but will do something soon!)")
        #return

        if "gachaLoot" not in user_data:
            user_data["gachaLoot"] = {}
        if "skinLoot" not in user_data:
            user_data["skinLoot"] = {}
        gacha_loot = user_data["gachaLoot"]
        #skin_loot = user_data["skinLoot"]

        if ctx.message.guild == None:
            await ctx.send(
                f"{ctx.author.mention}, you can only use this command in a guild."
            )
            return
        guild = ctx.message.guild.id
        if "favouriteGachaItem" not in user_data:
            await ctx.send(
                f"{ctx.author.mention}, you must select a favourite item before joining the raid! To do so, use `ricky setfavourite <item name>`."
            )
            return
        selected_item = user_data['favouriteGachaItem']
        star_level = self.get_star_value(selected_item)
        level = pow(5, self.STAR_NUMBER_CONVERSION[star_level] -
                    3) * gacha_loot[selected_item]
        user_hp = self.STATS[selected_item]["health"] * level / 20
        if guild not in CURRENT_RAIDS:
            CURRENT_RAIDS[guild] = {}
            CURRENT_RAIDS[guild]["new_raiders"] = {}
            CURRENT_RAIDS[guild]["participants"] = {}
            CURRENT_RAIDS[guild]["accept_raid_requests"] = True
            CURRENT_RAIDS[guild]["participants"][user_id] = {
                "item": selected_item,
                "level": level,
                "health": user_hp,
                "max_health": user_hp,
                "author": ctx.author
            }
            await ctx.send(
                f"**A raid is starting! Join at any time by using** `ricky raidboss`!"
            )
            await ctx.send(
                f"{ctx.author.mention}, you have joined the raid with your **{selected_item}! (Lvl. {level})**"
            )

            boss_item, boss_star_quality, boss_skin = self.select_item(
                0, 0, {})
            boss_display_embed = self.create_gacha_embed(
                boss_item, boss_skin, boss_star_quality, await
                my_bot.fetch_user(982167228248129546), {})
            boss_level = random.randint(level * 4 - level * 3,
                                        level * 4 + level * 3)
            boss_max_hp = self.STATS[boss_item]["health"] * boss_level / 20
            boss_current_hp = boss_max_hp
            boss_display_embed.add_field(name="Level",
                                         value=boss_level,
                                         inline=True)
            boss_pre_display_embed = discord.Embed(
                title="OMG!",
                description=
                f"A terrifying **{boss_item} (Lvl: {boss_level})** just appeared!",
                color=Color.green())
            await ctx.send(embed=boss_pre_display_embed)
            await ctx.send(embed=boss_display_embed)
            continue_raid = True
            await asyncio.sleep(2)
            await ctx.send(
                "The battle will commence in **15** seconds! Gather your raiders!."
            )
            await asyncio.sleep(15)
            #countdown_start_time = datetime.now()
            while continue_raid:
                number_one = random.uniform(1, 10000)
                number_two = random.uniform(1, 10000)
                question_embed = discord.Embed(
                    title="Quick!",
                    description=f"What is **{number_one} + {number_two}**? ")
                await ctx.send(embed=question_embed)
                countdown_start_time = datetime.now()
                answers = {}
                true_answer = number_one + number_two
                #allow raiders in (0th attempt)
                CURRENT_RAIDS[guild]["accept_raid_requests"] = False
                for new_entry in CURRENT_RAIDS[guild]["new_raiders"]:
                    CURRENT_RAIDS[guild]["participants"][
                        new_entry] = CURRENT_RAIDS[guild]["new_raiders"][
                            new_entry]
                CURRENT_RAIDS[guild]["new_raiders"].clear()
                CURRENT_RAIDS[guild]["accept_raid_requests"] = True

                try:
                    while True:
                        delta_time = datetime.now() - countdown_start_time
                        msg = await my_bot.wait_for("message",
                                                    timeout=5 -
                                                    delta_time.seconds,
                                                    check=check)
                        if str(msg.author.id) not in answers:
                            answers[str(msg.author.id)] = {
                                "content": msg.content
                            }
                        #print(msg)
                except:
                    #print(answers)
                    #await ctx.send(f"The correct answer was {number_one + number_two}. ")

                    #allow raiders in (1st attempt)
                    CURRENT_RAIDS[guild]["accept_raid_requests"] = False
                    for new_entry in CURRENT_RAIDS[guild]["new_raiders"]:
                        CURRENT_RAIDS[guild]["participants"][
                            new_entry] = CURRENT_RAIDS[guild]["new_raiders"][
                                new_entry]
                    CURRENT_RAIDS[guild]["new_raiders"].clear()
                    CURRENT_RAIDS[guild]["accept_raid_requests"] = True

                    for id in CURRENT_RAIDS[guild]["participants"]:
                        author = CURRENT_RAIDS[guild]["participants"][id][
                            "author"]
                        author_item_info = CURRENT_RAIDS[guild][
                            "participants"][id]
                        author_hp = author_item_info["health"]
                        if author_hp > 0:
                            author_item_name = author_item_info["item"]
                            author_multiplier = author_item_info["level"] / 20
                            author_answer_multiplier = 0.5
                            if id in answers:
                                try:
                                    #print("id and ans", answers[id]["content"])
                                    author_answer_multiplier_modifier = 1 - (
                                        abs(
                                            int(answers[id]["content"]) -
                                            true_answer) / true_answer)
                                except (ValueError):
                                    author_answer_multiplier_modifier = 0
                                author_answer_multiplier_modifier = max(
                                    author_answer_multiplier_modifier, 0)
                                author_answer_multiplier += author_answer_multiplier_modifier
                                print("mult: ", author_answer_multiplier)
                            #print("defence mult: ", self.STATS[author_item_info["item"]]["attack"] * math.log(author_item_info["level"]) / (self.STATS[boss_item]["defence"] * math.log(boss_level)), " godmode: ")
                            damage = self.STATS[author_item_info["item"]][
                                "attack"] * author_answer_multiplier * author_multiplier * (
                                    self.STATS[
                                        author_item_info["item"]]["attack"] *
                                    math.log(author_item_info["level"]) /
                                    (self.STATS[boss_item]["defence"] *
                                     math.log(boss_level + 1)))
                            boss_current_hp -= damage
                            #print(self.STATS[author_item_info["item"]]["attack"] * author_multiplier, (self.STATS[boss_item]["defence"] * boss_level / 20), ((self.STATS[author_item_info["item"]]["attack"] * author_multiplier) / (self.STATS[boss_item]["defence"] * boss_level / 20)))
                            attacking_embed = discord.Embed(
                                title="Attack!",
                                description=
                                f"**{author.mention}'s {author_item_name}** attacked the vile **{boss_item}**, dealing **{int(damage)} damage!** \n **{boss_item}** now has **{int(boss_current_hp)} of {int(boss_max_hp)} ({int((boss_current_hp/boss_max_hp)*100)}%)** health left!"
                            )
                            await ctx.send(embed=attacking_embed)
                            await asyncio.sleep(2)
                    if boss_current_hp < 1:
                        victory_embed = discord.Embed(
                            title="End of Raid: Victory",
                            description=
                            f"The evil **{boss_item}** has been slain; everyone earns some rewards.",
                            color=Color.blue())
                        await ctx.send(embed=victory_embed)
                        for participant in CURRENT_RAIDS[guild][
                                "participants"]:
                            #print("victory", participant)
                            participant_author = CURRENT_RAIDS[guild][
                                "participants"][participant]["author"]
                            participant_data = self.get_data(
                                participant_author)

                            #get participant loot
                            participant_gacha_loot = participant_data["gachaLoot"]
                            #get participant skins:
                            participant_skin_loot = participant_data["skinLoot"]

                            current_item, star_quality, current_skin = self.select_item(
                                20, 250, user_data)
                            six_star_chance = 0.001 * math.log(boss_level)
                            print("6stars chance: ", six_star_chance)
                            dice = random.uniform(0, 1)
                            if dice < six_star_chance:
                                star_quality = "Exclusive"
                                current_item = random.choice(
                                    list(self.SIX_STAR_DATA))

                            #grant item:
                            if current_item not in participant_gacha_loot:
                                participant_gacha_loot[current_item] = 0
                            participant_gacha_loot[current_item] += 1

                            #add necessary properties
                            if current_skin != None:
                                if current_item not in participant_skin_loot:
                                    participant_skin_loot[current_item] = {}
                                if current_skin[
                                        1] not in participant_skin_loot[
                                            current_item]:
                                    participant_skin_loot[current_item][
                                        current_skin[1]] = False

                            participant_data["gachaLoot"] = participant_gacha_loot
                            participant_data["skinLoot"] = participant_skin_loot
                            CACHE[participant] = copy.copy(participant_data)
                            victory_item_embed = self.create_gacha_embed(
                                current_item, None, star_quality,
                                participant_author, {})
                            await ctx.send(embed=victory_item_embed)
                            await asyncio.sleep(2)
                        continue_raid = False
                        CURRENT_RAIDS.pop(guild)
                        break
                    boss_possible_targets = []
                    for id in CURRENT_RAIDS[guild]["participants"]:
                        if CURRENT_RAIDS[guild]["participants"][id][
                                "health"] > 0:
                            boss_possible_targets.append(id)
                    boss_mult = boss_level / 20
                    boss_target = random.choice(boss_possible_targets)
                    boss_target_info = CURRENT_RAIDS[guild]["participants"][
                        boss_target]
                    inflicted_damage = self.STATS[boss_item][
                        "attack"] * boss_mult * (
                            self.STATS[boss_item]["attack"] *
                            math.log(boss_level) /
                            (self.STATS[boss_target_info["item"]]["defence"] *
                             math.log(boss_target_info["level"] + 1)))
                    #print("inflection:", self.STATS[boss_item]["attack"] * math.log(boss_level) / (self.STATS[boss_target_info["item"]]["defence"] * math.log(boss_target_info["level"] + 1)))
                    CURRENT_RAIDS[guild]["participants"][boss_target][
                        "health"] -= inflicted_damage
                    targeted_author = boss_target_info["author"]
                    targeted_item = boss_target_info["item"]
                    max_hp = boss_target_info["max_health"]
                    hp = boss_target_info["health"]
                    defending_embed = discord.Embed(
                        title="Attack!",
                        description=
                        f"The evil **{boss_item}** lashes out at **{targeted_author.mention}'s {targeted_item}**, dealing **{int(inflicted_damage)}** damage!\n **{targeted_item}** now has **{int(hp)} of {int(max_hp)} ({int(hp / max_hp*100)}%)** health left!",
                        color=Color.red())
                    await ctx.send(embed=defending_embed)
                    await asyncio.sleep(2)

                    #allow raiders in (2)
                    CURRENT_RAIDS[guild]["accept_raid_requests"] = False
                    for new_entry in CURRENT_RAIDS[guild]["new_raiders"]:
                        CURRENT_RAIDS[guild]["participants"][
                            new_entry] = CURRENT_RAIDS[guild]["new_raiders"][
                                new_entry]
                    CURRENT_RAIDS[guild]["new_raiders"].clear()
                    CURRENT_RAIDS[guild]["accept_raid_requests"] = True

                    alive_players = 0
                    for id in CURRENT_RAIDS[guild]["participants"]:
                        if CURRENT_RAIDS[guild]["participants"][id][
                                "health"] > 0:
                            alive_players += 1
                    if alive_players == 0:
                        defeat_embed = discord.Embed(
                            title="End of Raid: Defeat",
                            description=
                            f"The evil **{boss_item}** triumphs; all players have fallen!",
                            color=Color.red())
                        await ctx.send(embed=defeat_embed)
                        continue_raid = False
                        CURRENT_RAIDS.pop(guild)
                        break
        else:
            if user_id not in CURRENT_RAIDS[guild][
                    "participants"] and user_id not in CURRENT_RAIDS[guild][
                        "new_raiders"]:
                if CURRENT_RAIDS[guild]["accept_raid_requests"]:
                    CURRENT_RAIDS[guild]["new_raiders"][user_id] = {
                        "item": selected_item,
                        "level": level,
                        "health": user_hp,
                        "max_health": user_hp,
                        "author": ctx.author
                    }
                    await ctx.send(
                        f"{ctx.author.mention}, you have joined the raid with your **{selected_item}! (Lvl. {level})** and will be able to move on the following turn."
                    )
                else:
                    await ctx.send(
                        f"{ctx.author.mention}, please wait a moment, and then try that again!"
                    )
            else:
                await ctx.send(
                    f"{ctx.author.mention}, you are already in the raid!")

    @commands.command()
    async def setfavourite(self, ctx):
        global CACHE
        user_data = self.get_data(ctx.author)
        user_id = str(ctx.author.id)
        user_request = ctx.message.content.split(" ")
        if len(user_request) > 2:
            item_request = " ".join(user_request[2:])
            #allow people to set skin as favourite, this just sets the item to favourite but autoequips the skin anyway.
            item_request, should_equip_skin, original_skin = self.skin_to_item_if_possible(
                item_request)
            if "gachaLoot" not in user_data:
                user_data["gachaLoot"] = {}
            if "skinLoot" not in user_data:
                user_data["skinLoot"] = {}
            gacha_loot = user_data["gachaLoot"]
            skin_loot = user_data["skinLoot"]

            if item_request.lower(
            ) not in self.EASY_ITEM_NAMES or self.EASY_ITEM_NAMES[
                    item_request.lower()] not in gacha_loot:
                await ctx.send(
                    f"{ctx.author.mention}, invalid request! You don't have the item or it doesn't exist."
                )
            else:
                item_request = self.EASY_ITEM_NAMES[item_request.lower()]
                #self.useskin(ctx)
                if should_equip_skin:
                    user_data, success_status = self.change_equipped_skin(
                        user_data, item_request, original_skin)
                    if success_status == -1:
                        await ctx.send(
                            f"{ctx.author.mention}, you don't have that skin!")
                    elif success_status == 0:
                        await ctx.send(
                            f"{ctx.author.mention}, **{original_skin}** for **{item_request}** has been **unequipped!**"
                        )
                    elif success_status == 1:
                        await ctx.send(
                            f"{ctx.author.mention}, **{original_skin}** for **{item_request}** has been **selected!**"
                        )
                selected_skin = None
                selected_star_quality = self.get_star_value(item_request)
                if item_request in skin_loot:
                    for skin in skin_loot[item_request]:
                        if skin_loot[item_request][skin]:
                            for matching_skin in self.SKIN_DATA[item_request]:
                                if matching_skin[1] == skin:
                                    selected_skin = matching_skin[1]
                                    if selected_star_quality == "4":
                                        selected_star_quality = "Special"
                                    elif selected_star_quality == "5":
                                        selected_star_quality = "Exquisite"
                                    break
                user_data["favouriteGachaItem"] = item_request
                await ctx.send(
                    f"{ctx.author.mention}, **{item_request}** **(Skin: {selected_skin})** is now set as your favourite item!"
                )
        else:
            if "favouriteGachaItem" in user_data:
                user_data.pop("favouriteGachaItem")
            await ctx.send(
                f"{ctx.author.mention}, you no longer have a favourite item.")
        CACHE[user_id] = copy.copy(user_data)

    @commands.command()
    async def useskin(self, ctx):
        global CACHE
        user_data = self.get_data(ctx.author)
        user_id = str(ctx.author.id)
        #test = True

        user_request = ctx.message.content.split(" ")
        if len(user_request) > 2:
            skin_request = " ".join(user_request[2:])
            selected_item = None
            selected_skin = None
            for item in self.SKIN_DATA:
                for skin in self.SKIN_DATA[item]:
                    if skin[1].lower() in skin_request.lower():
                        selected_item = item
                        selected_skin = skin[1]
                        break
            if selected_item == None:
                await ctx.send(
                    f"{ctx.author.mention}, that skin does not exist!")
            else:
                user_data, success_status = self.change_equipped_skin(
                    user_data, selected_item, selected_skin)
                if success_status == -1:
                    await ctx.send(
                        f"{ctx.author.mention}, you don't have that skin!")
                elif success_status == 0:
                    await ctx.send(
                        f"{ctx.author.mention}, **{selected_skin}** for **{selected_item}** has been **unequipped!**"
                    )
                elif success_status == 1:
                    await ctx.send(
                        f"{ctx.author.mention}, **{selected_skin}** for **{selected_item}** has been **selected!**"
                    )
        else:
            await ctx.send(
                f"{ctx.author.mention}, invalid request! Do `ricky useskin <Skin Name>`."
            )
        CACHE[user_id] = copy.copy(user_data)

    @commands.command()
    async def displayitem(self, ctx):
        global CACHE
        user_data = self.get_data(ctx.author)
        user_id = str(ctx.author.id)
        item_request = ""
        user_request = ctx.message.content.split(" ")
        if "gachaLoot" not in user_data:
            user_data["gachaLoot"] = {}
        if "skinLoot" not in user_data:
            user_data["skinLoot"] = {}
        gacha_loot = user_data["gachaLoot"]
        skin_loot = user_data["skinLoot"]
        if len(user_request) > 2:
            item_request = " ".join(user_request[2:])
            item_request, should_equip_skin, original_skin = self.skin_to_item_if_possible(
                item_request)
        elif "favouriteGachaItem" in user_data:
            item_request = user_data["favouriteGachaItem"]
            should_equip_skin = False
        else:
            await ctx.send(
                f"{ctx.author.mention}, invalid request! Do `ricky displayitem <Item Name>`."
            )
            return

        if item_request.lower(
        ) not in self.EASY_ITEM_NAMES or self.EASY_ITEM_NAMES[
                item_request.lower()] not in gacha_loot:
            await ctx.send(
                f"{ctx.author.mention}, invalid request! You don't have the item or it doesn't exist."
            )
        else:
            item_request = self.EASY_ITEM_NAMES[item_request.lower()]
            if should_equip_skin:
                user_data, success_status = self.change_equipped_skin(
                    user_data, item_request, original_skin)
                if success_status == -1:
                    await ctx.send(
                        f"{ctx.author.mention}, you don't have that skin!")
                elif success_status == 0:
                    await ctx.send(
                        f"{ctx.author.mention}, **{original_skin}** for **{item_request}** has been **unequipped!**"
                    )
                elif success_status == 1:
                    await ctx.send(
                        f"{ctx.author.mention}, **{original_skin}** for **{item_request}** has been **selected!**"
                    )
            selected_skin = None
            selected_star_quality = self.get_star_value(item_request)
            if item_request in skin_loot:
                for skin in skin_loot[item_request]:
                    if skin_loot[item_request][skin]:
                        for matching_skin in self.SKIN_DATA[item_request]:
                            if matching_skin[1] == skin:
                                selected_skin = matching_skin
                                if selected_star_quality == "4":
                                    selected_star_quality = "Special"
                                elif selected_star_quality == "5":
                                    selected_star_quality = "Exquisite"
                                break
                #print(item_request, selected_skin, self.get_star_value(item_request), ctx.author, {})

            my_embed = self.create_gacha_embed(item_request, selected_skin,
                                               selected_star_quality,
                                               ctx.author, {})
            my_embed.add_field(name="Amount", value=gacha_loot[item_request])
            await ctx.send(embed=my_embed)
        CACHE[user_id] = copy.copy(user_data)

    @commands.command()
    async def gacha(self, ctx):
        global CACHE
        user_data = self.get_data(ctx.author)
        user_id = str(ctx.author.id)

        #if user_id != "328039243303616523":
        #    return

        if "gachaWishCount" not in user_data:
            user_data["gachaWishCount"] = 10
        if "gachaCooldown" not in user_data:
            user_data["gachaCooldown"] = (
                datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        if "gachaLoot" not in user_data:
            user_data["gachaLoot"] = {}
        if "skinLoot" not in user_data:
            user_data["skinLoot"] = {}
        gacha_loot = user_data["gachaLoot"]
        skin_loot = user_data["skinLoot"]
        #print(gacha_loot, "Loot.\n")
        #get 10 wishes per 3 hours.
        cooldown_time = datetime.strptime(user_data["gachaCooldown"],
                                          "%Y-%m-%d %H:%M:%S")
        delta_time = datetime.now() - cooldown_time
        #print("cooldown: ", cooldown_time, " deltatime ", delta_time, " dts ", delta_time.seconds)
        #if delta_time.seconds > 18000 or delta_time.days > 0:
        if delta_time.days > 0:
            user_data["gachaWishCount"] = 10
        else:
            user_data["gachaWishCount"] = user_data["gachaWishCount"] + delta_time.seconds / 1800
            if user_data["gachaWishCount"] > 10:
                user_data["gachaWishCount"] = 10


        #for testing only
        #if user_id == "328039243303616523":
        #    user_data["gachaWishCount"] = 10
        #print("Database ID:", id(db[user_id]), "Cache ID:", id(user_data))
        #print("Database Things:", db[user_id], "Cache Things:", user_data)
        #user_data["gachaWishCount"] = True
        #gacha_loot["Nanahira"] += 5
        #print("Database Things:", db[user_id], "\n\nCache Things:", CACHE[user_id], "\n\nUSERDATA THINGS:", user_data, "\n\n\n\n\n")

        if user_data["gachaWishCount"] > 0:
            #make up for lost time pulls:
            number_of_pulls = 1#round(
                #(delta_time.days * 86400 + delta_time.seconds) / 1800)
            await ctx.send(
                f"""{ctx.author.mention} has unleashed **{number_of_pulls}** pulls!!, and has **{user_data["gachaWishCount"] - 1}** pulls left."""
            )
            #print(number_of_pulls)
            #return
            user_data["gachaWishCount"] -= number_of_pulls
            user_data["gachaCooldown"] = (
                datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            current_pulls = {}
            best_pull = ""
            best_skin = None
            best_pull_rating = "MIN"
            #add necessary properties
            if "gachaPullsSince5Star" not in user_data:
                user_data["gachaPullsSince5Star"] = 0
            if "gachaPullsSince4Star" not in user_data:
                user_data["gachaPullsSince4Star"] = 0
            pulls_since_5 = user_data["gachaPullsSince5Star"]
            pulls_since_4 = user_data["gachaPullsSince4Star"]

            for i in range(number_of_pulls):
                #get item info
                current_item, star_quality, current_skin = self.select_item(
                    pulls_since_4, pulls_since_5, user_data)

                #add to user loot
                if current_item not in gacha_loot:
                    gacha_loot[current_item] = 0
                gacha_loot[current_item] += 1

                #add necessary properties
                if current_skin != None:
                    if current_item not in skin_loot:
                        skin_loot[current_item] = {}
                    if current_skin[1] not in skin_loot[current_item]:
                        skin_loot[current_item][current_skin[1]] = False

                #add to items to be displayed
                if current_item not in current_pulls:
                    current_pulls[current_item] = 0
                current_pulls[current_item] += 1

                if self.BEST_PULL_RATINGS[
                        best_pull_rating] < self.BEST_PULL_RATINGS[
                            star_quality]:
                    best_pull = current_item
                    best_pull_rating = star_quality
                    best_skin = current_skin

                if self.STAR_NUMBER_CONVERSION[star_quality] == 3:
                    pulls_since_5 += 1
                    pulls_since_4 += 1
                elif self.STAR_NUMBER_CONVERSION[star_quality] == 4:
                    pulls_since_5 += 1
                    pulls_since_4 = 0
                else:
                    pulls_since_5 = 0
                    pulls_since_4 += 1

            #put mutated fields back into cache
            user_data["gachaLoot"] = gacha_loot
            user_data["skinLoot"] = skin_loot
            user_data["gachaPullsSince5Star"] = pulls_since_5
            user_data["gachaPullsSince4Star"] = pulls_since_4

            my_embed = self.create_gacha_embed(best_pull, best_skin,
                                               best_pull_rating, ctx.author,
                                               current_pulls)
            await ctx.send(embed=my_embed)
        else:
            await ctx.send(
                f"{ctx.author.mention},  your wishes are not ready right now! Your next 10-pull is in **{(10800 - delta_time.seconds)//60} minutes and {(10800 - delta_time.seconds)%60} seconds. ({cooldown_time + timedelta(seconds=10800) - timedelta(seconds=25200)})**"
            )
        CACHE[user_id] = copy.copy(user_data)
        #print("Database Things:", db[user_id], "\n\nCache Things:", CACHE[user_id], "\n\nUSERDATA THINGS:", user_data)


#@my_bot.command("copypasta")
#async def command_copypasta(message):
#    global limit, current_time, refresh_time, token
#    if limit > 10:
#        headers = {
#            'Authorization': token,
#            'User-Agent': 'ricky-simulator by u/BetaThunder'
#        }
#        r = requests.get(API_URL + '/r/copypasta/random', headers=headers)
#        if int(r.status_code) != 200:
#            print("Refreshing auth token!")
#            token = refresh_token()
#        limit = int(r.headers['X-Ratelimit-Remaining'])
#        current_time = datetime.now()
#        refresh_time = datetime.now() + timedelta(
#            seconds=int(r.headers['X-Ratelimit-Reset']))
#        values = r.json()[0]
#        pasta = values['data']['children'][0]['data']['selftext']
#        #replacement for safety
#        if "nigg" not in pasta.lower():
#            await message.channel.send(str(pasta[0:1999]))
#    else:
#        if datetime.now() < refresh_time:
#            await message.channel.send("Stop spamming me for the next " +
#                                       str((refresh_time -
 #                                           datetime.now()).seconds) +
#                                       " seconds, alright?")
#        else:
 #           limit = 300


@my_bot.command()
async def print_hi(ctx):
    print("Hi")
    await ctx.send("Hi.")


@my_bot.event
async def on_ready():
    global CACHE
    print("Grabbing data:")
    with open("USER_DATA.gachasavedata", "r", encoding='utf-8') as savefile:
        #print(savefile.read())
        CACHE = eval(savefile.read())
    print("I'm ready to go!")
    my_bot.loop.create_task(autosave())


#website setup
#app = Flask("myApp")


#def appRun():
#    app.run(host='0.0.0.0', port=8080)


#@app.route("/")
#def begin():
#    return render_template(
#       'base.html',  # Template file path, starting from the templates folder.
#   )


#Go!
#token = refresh_token()
#myThread = Thread(target=appRun)
#myThread.start()
my_bot.add_cog(Gacha(my_bot))
my_bot.run(TOKEN)
#r = requests.get("http://127.0.0.1:5000")
