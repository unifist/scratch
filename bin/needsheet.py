#!/usr/bin/env python

import re
import json
import gsheets
import discord
import github

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # Create Listing
        if message.content.startswith("+lis"):
            listing = message.content.split()[1]
            if len(listing) > 1:
                await message.reply(f"Create Listing: {listing}?", mention_author=True)

    async def on_reaction_add(self, reaction, user):

        # Create Listing
        if (
            self.user.id == reaction.message.author.id and
            reaction.message.content.startswith("Create Listing: ") and
            reaction.message.content.endswith("?") and
            reaction.emoji == '👍'
        ):

            name = reaction.message.content[len("Create Listing: "):-len("?")]
            gspread_client = gsheets.connect()
            base = gspread_client.open("Outreach Development Base")

            gspread_client.copy(base.id, title=f"Outreach Development {name}")
            listing_url = gspread_client.open(f"Outreach Development {name}").url
            await reaction.message.edit(content=f"Created Listing: {name} - {listing_url}.")


with open("/opt/service/secret/discord.json", "r") as creds_file:
        token = json.load(creds_file)["token"]

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
