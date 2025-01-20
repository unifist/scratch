#!/usr/bin/env python

import json

import atproto

import bsky
import gsheets
import outreach

client, profile = bsky.connect()
gspread_client = gsheets.connect()
outreach_config = outreach.config()

for source in gspread_client.open(f"Outreach Source - {outreach_config['link']}").worksheet("Sources").get_all_records():

    if source["Link"] and source["Status"] == "Active":

        text_builder = atproto.client_utils.TextBuilder()
        text_builder.link(source["Link"], source["Link"])

        if source["Description"]:
            text_builder.text("\n\n")
            text_builder.text(source["Description"])

        root_post_ref = atproto.models.create_strong_ref(client.send_post(text_builder))

        resources = [f"{header}: {source[header]}" for header in ["Categories", "Provides", "Needs"] if source[header]]

        if resources:
            client.send_post(
                "\n\n".join(resources),
                reply_to=atproto.models.AppBskyFeedPost.ReplyRef(parent=root_post_ref, root=root_post_ref),
            )
