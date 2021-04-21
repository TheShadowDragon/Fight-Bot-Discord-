import discord
from discord.ext import commands
import random
import os
import asyncio
import subprocess
import json
from pathlib import Path
import wget
import math
import requests
import time
import sys
import logging

client = discord.Client()
client = commands.Bot(command_prefix = '$')

#Public Class
class Fighters:
  def __init__(self, challenger, Enemy, Accept):
    self.challenger = challenger
    self.Enemy = Enemy
    self.Accept = False



#Random things from WearyBot lol idk what any of it does
@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(message, filename = "Players.json"):

    if message.author == client.user:
        return
    print('(', message.guild.name, ')',message.author, ':', message.content)

############
#FUNCTIONS
############

    #Function to add player to player database
    def add_player(user = message.author, filename = "Players.json"):
      with open (filename,'r') as f:
        users = json.load(f)
      
      whoWins = (f"{message.author.mention}Wins")
      whoLoses = (f"{message.author.mention}Losses")

      if whoWins in users and whoLoses in users:
        return False;  
      
      else:
        users[whoWins] = 0
        users[whoLoses] = 0

      with open (filename, 'w') as f:
        json.dump(users,f)

    #updates the player's win/loss        
    def update_player(user):
      add_player()
      with open (filename,'r') as f:
       users = json.load(f)
      
      with open (filename, "w") as f:
        json.dump(users,f)
        
      users[user] += 1

      with open (filename, "w") as f:
        json.dump(users,f)

    #fight function
    async def FuncFight():
        RandomWeapon = ["sword", "rock", "tomato", "finger", "grass", "computer", "cup", "steak", "dishwasher", "bouncy ball", "tooth", "sledgehammer"]
        RandomSenario = ["mauled", "stabbed", "scratched", "punched", "petted", "licked", "scratched", "thrown", "slapped", "slapped", "uwu'd", "anime'd"]
        RandomWinner = [Fighters.challenger, message.author]

        WeaponChooser = random.choice(RandomWeapon)
        SenarioChooser = random.choice(RandomSenario)
        WinnerChooser = random.choice(RandomWinner)

        if WinnerChooser == Fighters.challenger: 
            await message.channel.send(f"{message.author.mention} was {SenarioChooser} with a {WeaponChooser} by {Fighters.challenger}")

            update_player(f"{Fighters.challenger}Losses")
            update_player(f"{message.author.mention}Wins")
        else:
            await message.channel.send(f"{Fighters.challenger} was {SenarioChooser} with a {WeaponChooser} by {message.author.mention}")

            update_player(f"{message.author.mention}Wins")
            update_player(f"{Fighters.challenger}Losses")

      



    #Timer function. A sort of fight deny before I actually add the commands. It also counts as a time limit. Raise from 15?
    async def FuncTimer(t = 0):

      while t <= 15:
        await asyncio.sleep(1)
        t += 1



      if t > 15:
        if Fighters.Accept == True:
          t = 0
          Fighters.Accept = False
          Fighters.challenger = "None"
          Fighters.Enemy = "None"
          Fighters.Accept = False
          t = 0
        else:
          await message.channel.send(f"{message.author.mention} Your enemy was either too late to accept, or they were a coward. Shame!")
          Fighters.challenger = "None"
          Fighters.Enemy = "None"
          Fighters.Accept = False
          t = 0
        
        

##############
#COMMANDS
#############

#profile command
    if message.content.startswith('$fipr'):

        add_player()
        user = message.author.mention

        with open (filename,'r') as f:
          users = json.load(f)
        
        with open (filename, "w") as f:
          json.dump(users,f)



        win_amount = users[f"{user}Wins"]
        loss_amount = users[f"{user}Losses"]

        em = discord.Embed(title = f"{user}'s wins", color = discord.Color.green())
        em.add_field(name = "wins", value = win_amount)
        em.add_field(name = "losses", value = loss_amount)
        await message.channel.send(embed = em)


    #Fight request
    if message.content.startswith("$fight"):
        add_player()
        user = message.author

        Contents = message.content.replace('$fight ', '')
        if message.author.mention != Contents:
          if '@' in message.content:
            request = True

            Fighters.challenger = message.author.mention
            Fighters.Enemy = Contents

            await message.channel.send(f"{Contents} was challenged to a duel by {message.author.mention}! Do $faccept {message.author.mention} if you accept!")
            Fighters.Accept = False
            await FuncTimer()

          else:
            await message.channel.send("You can't just fight a imaginary friend you crank!")
        else:
          await message.channel.send("You can't fight yourself you crazy bastard")



    #Accept Command
    if message.content.startswith('$faccept'):


        add_player()
        input = message.content.replace('$faccept ', '')
        
        if message.author.mention != Fighters.Enemy:

          if Fighters.challenger != message.content:

            await message.channel.send(f"{message.author.mention} has accepted the duel from {Fighters.challenger}!")
            Fighters.Accept = True
            await FuncFight();


          else:
                await message.channel.send("You have requested to accept from the wrong person, or no one has requested to fight you")
        else:
          await message.channel.send("No one challenged YOU silly")
    


my_secret = os.environ['Bot_ID']
client.run(my_secret)
