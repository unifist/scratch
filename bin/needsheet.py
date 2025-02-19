#!/usr/bin/env python

import re
import json
import Levenshtein
import gsheets
import discord
import github
import outreach

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        self.outreach = outreach.API()

    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # List Listings
        if message.content.startswith("*lis"):

            listings = self.outreach.list_listings()

            for listing in listings:
                await message.reply(f"Listing: {' - '.join(listing)}.", mention_author=True)

        # Create Listing
        elif message.content.startswith("+lis"):

            listings = self.outreach.parse_listings(message.content)

            for listing in listings:
                await message.reply(f"Create Listing: {listing}?", mention_author=True)

        # List Categories
        elif message.content.startswith("*cat"):

            if " " not in message.content:
                await message.reply(f"Usage: *cat/egory (Listing)", mention_author=True)
                return

            listing, categories = self.outreach.list_categories(message.content.split(" ", 1)[1])

            for category in categories:
                await message.reply(f"Category: {' - '.join([listing] + category)}.", mention_author=True)

        # Create Category
        elif message.content.startswith("+cat"):

            if not " - " in message.content and "\n" not in message.content:
                await message.reply(f"Usage: +cat/egory (Listing) -|\\n Name (- Description: optional) \\n...", mention_author=True)
                return

            listing, categories = self.outreach.parse_categories(message.content.split(" ", 1)[1])

            for category in categories:
                await message.reply(f"Create Category: {listing} - {category}?", mention_author=True)

        # List Resources
        elif message.content.startswith("*res"):

            if " " not in message.content:
                await message.reply(f"Usage: *res/source (Listing)", mention_author=True)
                return

            listing, resources = self.outreach.list_resources(message.content.split(" ", 1)[1])

            for resource in resources:
                await message.reply(f"Resource: {' - '.join([listing] + resource)}.", mention_author=True)


        # Create Resource
        elif message.content.startswith("+res"):

            if " - " not in message.content and "\n" not in message.content:
                await message.reply(f"Usage: +res/source (Listing) -|\\n Name (- Description: optional) \\n...", mention_author=True)
                return

            listing, resources = self.outreach.parse_resources(message.content.split(" ", 1)[1])

            for resource in resources:
                await message.reply(f"Create Resource: {listing} - {resource}?", mention_author=True)

        # List Sources
        elif message.content.startswith("*sou"):

            if " " not in message.content:
                await message.reply(f"Usage: *sou/rce (Listing)", mention_author=True)
                return

            listing, sources = self.outreach.list_sources(message.content.split(" ", 1)[1])

            for source in sources:
                await message.reply(f"Source: {'\n'.join([listing] + source)}", mention_author=True)

        # Find Source
        elif message.content.startswith("+sou"):

            if " - " not in message.content and "\n" not in message.content:
                await message.reply(f"Usage: +sou/rce (Listing) +cat +res -|\\n (link|name)\\n...", mention_author=True)
                return

            listing, catres, sources = self.outreach.parse_sources(message.content.split(" ", 1)[1])

            for source in sources:
                await message.reply(f"Create Source: {listing} {catres}- {source}?", mention_author=True)


    async def on_reaction_add(self, reaction, user):

        # Create Listing
        if (
            self.user.id == reaction.message.author.id and
            reaction.message.content.startswith("Create Listing: ") and
            reaction.message.content.endswith("?") and
            reaction.emoji == '👍'
        ):

            listing, listing_url = self.outreach.create_listing(reaction.message.content[len("Create Listing: "):-len("?")])

            await reaction.message.edit(content=f"Created Listing: {listing}\n{listing_url}.")

        # Create Category
        if (
            self.user.id == reaction.message.author.id and
            reaction.message.content.startswith("Create Category: ") and
            reaction.message.content.endswith("?") and
            reaction.emoji == '👍'
        ):

            listing, category = self.outreach.create_category(reaction.message.content[len("Create Category: "):-len("?")])

            await reaction.message.edit(content=f"Created Category: {listing} - {category}.")

        # Create Resource
        if (
            self.user.id == reaction.message.author.id and
            reaction.message.content.startswith("Create Resource: ") and
            reaction.message.content.endswith("?") and
            reaction.emoji == '👍'
        ):

            listing, resource = self.outreach.create_resource(reaction.message.content[len("Create Resource: "):-len("?")])

            await reaction.message.edit(content=f"Created Resource: {listing} - {resource}.")

        # Create Source
        if (
            self.user.id == reaction.message.author.id and
            reaction.message.content.startswith("Create Source: ") and
            reaction.message.content.endswith("?") and
            reaction.emoji == '👍'
        ):

            listing_catres_source = self.outreach.create_source(reaction.message.content[len("Create Source: "):-len("?")])

            await reaction.message.edit(content=f"Created Source: {listing_catres_source}.")


with open("/opt/service/secret/discord.json", "r") as creds_file:
    token = json.load(creds_file)["token"]

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
