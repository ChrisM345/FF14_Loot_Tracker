import csv
import requests
from discord_webhook import url
import discord
from datetime import date
from char_to_fc import characterToFC

today = date.today()

#loot values for salvage
lootValue = {
    "Salvaged Ring": 8000,
    "Salvaged Bracelet": 9000,
    "Salvaged Earring": 10000,
    "Salvaged Necklace": 13000,
    "Extravagant Salvaged Ring": 27000,
    "Extravagant Salvaged Bracelet": 28500,
    "Extravagant Salvaged Earring": 30000,
    "Extravagant Salvaged Necklace": 34500,
}

def trackLoot(data):
    loot = data
    lootPerCharacter = {} # use dictionary to store total money made by each character


    #Go through data and created a nested dictionary with {char: {lootName : quantity}}
    for data in loot.playerLoot:
        name = data.Name
        name = characterToFC[name] #change my character name to the name of the fc using dictionary
        loot = data.LootName
        quantity = data.Quantity
        if lootPerCharacter.get(name) == None:
            lootPerCharacter[name] = {loot: quantity}
        else:
            lootPerCharacter[name].update({loot: quantity + lootPerCharacter.get(name,{}).get(loot, 0)})

    #Separate info for each character as a string.
    characterOne = ""
    characterOneLoot = ""

    characterTwo = ""
    characterTwoLoot = ""

    characterThree = ""
    characterThreeLoot = ""

    characterFour = ""
    characterFourLoot = ""

    characterFive = ""
    characterFiveLoot = ""

    characterSix = ""
    characterSixLoot = ""


    totalMoneyEarned = 0
    charLootAll = []

    #Go through the nested dictionary and compile data into a list format where the order is [character, [total + loot]]
    lootPerCharacterTotal = {}
    #simple csv file with date, fc name, and total
    with open(r'C:\Users\Chris\Documents\Code\FF14_Loot_Tracker\LootCSV.csv', 'a', newline='') as file:
        for char, data in lootPerCharacter.items():
            total = 0
            charLootAll.append(char)
            charactersLoot = ""
            for item, quantity in data.items():
                total += lootValue.get(item, 0) * quantity
                charactersLoot += item
                charactersLoot += " x" +str(quantity)+"\n"
            lootPerCharacterTotal[char] = total
            charLootAll.append(str(format(total,',d')) +"\n"+charactersLoot)
            totalMoneyEarned += total
            writer = csv.writer(file)
            newCSVRow = [today.strftime("%b-%d-%Y"), char, total]
            writer.writerow(newCSVRow)

    #manually assign data from list into separate variables
    characterOne = charLootAll[0]
    characterOneLoot = charLootAll[1]


    embed = discord.Embed(title="Salvage Report - " + today.strftime("%b-%d-%Y"),
                        description="Total: "+ str(format(totalMoneyEarned, ',d')),
                        colour=0x00b0f4)

    embed.add_field(name=characterOne,
                    value=characterOneLoot,
                    inline=True)

    embed.add_field(name=characterTwo,
                    value=characterTwoLoot,
                    inline=True)

    embed.add_field(name=characterThree,
                    value=characterThreeLoot,
                    inline=True)

    embed.add_field(name=characterFour,
                    value=characterFourLoot,
                    inline=True)

    embed.add_field(name=characterFive,
                    value=characterFiveLoot,
                    inline=True)

    embed.add_field(name=characterSix,
                    value=characterSixLoot,
                    inline=True)

    webhook = discord.SyncWebhook.from_url(url)
    webhook.send(embed=embed)