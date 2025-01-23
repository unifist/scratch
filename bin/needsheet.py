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
            listing = message.content.split(" ", 1)[1]
            if len(listing) > 1:
                await message.reply(f"Create Listing: {listing}?", mention_author=True)

        # List Categories
        if message.content.startswith("*cat"):

            if " " not in message.content:
                await message.reply(f"Usage: *cat/egory (Listing)", mention_author=True)
                return

            gspread_client = gsheets.connect()

            listing = message.content.split(" ", 1)[1]
            listing = gsheets.closest(gspread_client, "Outreach Development Admin", "Listings", "Listing", listing)

            for category in gsheets.rows(gspread_client, f"Outreach Development {listing}", "Categories"):

                content = [listing, category['Category']]

                if category['Description']:
                    content.append(category['Description'])

                await message.reply(f"Category: {' - '.join(content)}.", mention_author=True)

        # Create Category
        if message.content.startswith("+cat"):

            if not " - " in message.content and "\n" not in message.content:
                await message.reply(f"Usage: +cat/egory (Listing) -|\\n Name (- Description: optional) \\n...", mention_author=True)
                return

            listing_category = message.content.split(" ", 1)[1]

            if "\n" in listing_category:
                categories = listing_category.split("\n")
                listing = categories.pop(0)
            elif " - " in listing_category:
                listing, category = listing_category.split(" - ", 1)
                categories = [category]

            gspread_client = gsheets.connect()
            listing = gsheets.closest(gspread_client, "Outreach Development Admin", "Listings", "Listing", listing)

            for category in categories:
                if len(category) > 1:
                    await message.reply(f"Create Category: {listing} - {category}?", mention_author=True)

        # List Resources
        if message.content.startswith("*res"):

            if " " not in message.content:
                await message.reply(f"Usage: *res/source (Listing)", mention_author=True)
                return

            gspread_client = gsheets.connect()

            listing = message.content.split(" ", 1)[1]
            listing = gsheets.closest(gspread_client, "Outreach Development Admin", "Listings", "Listing", listing)

            for resource in gsheets.rows(gspread_client, f"Outreach Development {listing}", "Resources"):

                content = [listing, resource['Resource']]

                if resource['Description']:
                    content.append(resource['Description'])

                await message.reply(f"Resource: {' - '.join(content)}.", mention_author=True)

        # Create Resource
        if message.content.startswith("+res"):

            if not " - " in message.content and "\n" not in message.content:
                await message.reply(f"Usage: +res/source (Listing) -|\\n Name (- Description: optional) \\n...", mention_author=True)
                return

            listing_resource = message.content.split(" ", 1)[1]

            if "\n" in listing_resource:
                resources = listing_resource.split("\n")
                listing = resources.pop(0)
            elif " - " in listing_resource:
                listing, resource = listing_resource.split(" - ", 1)
                resources = [resource]

            gspread_client = gsheets.connect()
            listing = gsheets.closest(gspread_client, "Outreach Development Admin", "Listings", "Listing", listing)

            for resource in resources:
                if len(resource) > 1:
                    await message.reply(f"Create Resource: {listing} - {resource}?", mention_author=True)


    async def on_reaction_add(self, reaction, user):

        # Create Listing
        if (
            self.user.id == reaction.message.author.id and
            reaction.message.content.startswith("Create Listing: ") and
            reaction.message.content.endswith("?") and
            reaction.emoji == '👍'
        ):

            listing = reaction.message.content[len("Create Listing: "):-len("?")]
            description = ""

            if " - " in listing:
                name, description = listing.split(" - ", 1)
            else:
                name = listing

            gspread_client = gsheets.connect()
            base = gspread_client.open("Outreach Development Base")

            gspread_client.copy(base.id, title=f"Outreach Development {name}")
            listing_url = gspread_client.open(f"Outreach Development {name}").url

            listings = gspread_client.open("Outreach Development Admin").worksheet("Listings")
            listings.append_row([name, description], table_range="A1:B1")

            await reaction.message.edit(content=f"Created Listing: {listing}\n{listing_url}.")

        # Create Category
        if (
            self.user.id == reaction.message.author.id and
            reaction.message.content.startswith("Create Category: ") and
            reaction.message.content.endswith("?") and
            reaction.emoji == '👍'
        ):

            listing_category = reaction.message.content[len("Create Category: "):-len("?")]

            listing, category = listing_category.split(" - ", 1)

            description = ""

            if " - " in category:
                name, description = category.split(" - ", 1)
            else:
                name = category

            gspread_client = gsheets.connect()
            categories = gspread_client.open(f"Outreach Development {listing}").worksheet("Categories")
            categories.append_row([name, description], table_range="A1:B1")

            await reaction.message.edit(content=f"Created Category: {listing} - {category}.")

        # Create Resource
        if (
            self.user.id == reaction.message.author.id and
            reaction.message.content.startswith("Create Resource: ") and
            reaction.message.content.endswith("?") and
            reaction.emoji == '👍'
        ):

            listing_resource = reaction.message.content[len("Create Resource: "):-len("?")]

            listing, resource = listing_resource.split(" - ", 1)

            description = ""

            if " - " in resource:
                name, description = resource.split(" - ", 1)
            else:
                name = resource

            gspread_client = gsheets.connect()
            resources = gspread_client.open(f"Outreach Development {listing}").worksheet("Resources")
            resources.append_row([name, description], table_range="A1:B1")

            await reaction.message.edit(content=f"Created Resource: {listing} - {resource}.")


with open("/opt/service/secret/discord.json", "r") as creds_file:
        token = json.load(creds_file)["token"]

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
