#!/usr/bin/env python

import re
import json
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

        # if I should is anyehwer

        if "i should" in message.content.lower():

            # find all the action items best we can
            for action in [item.split('.')[0].strip() for item in re.split("i should", message.content, flags=re.IGNORECASE)]:
                if len(action) > 1:
                    await message.reply(f"Create: {action}?", mention_author=True)

    async def on_reaction_add(self, reaction, user):
        # we only care about our own tasks
        if (
            self.user.id != reaction.message.author.id or
            not reaction.message.content.startswith("Create: ") or
            not reaction.message.content.endswith("?")
        ):
            return

        action = reaction.message.content[8:-1]

        if reaction.emoji == '👍':
            item_url = github.QL("unifist", "unum").draft(action, reaction.message.jump_url)
            await reaction.message.edit(content=f"Created: {action} - {item_url}.")


with open("/opt/service/secret/discord.json", "r") as creds_file:
        token = json.load(creds_file)["token"]

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
