#!/usr/bin/env python

import json
import bsky

client, profile = bsky.connect()

print('Welcome,', profile.handle)

followers = client.get_followers(actor=profile.handle)

for follower in followers.followers:
    print(follower.handle)

response = client.app.bsky.feed.get_author_feed(params={
    "actor": "gaf3.com",
    "limit": 30,
    "filter": "posts_with_replies"
})

def post_to_dict(post):

    value = {
        "cid": view.post.cid,
        "author": view.post.author.handle,
        "created_at": view.post.record.created_at,
        "text": view.post.record.text
    }

    return value

for view in response.feed:
    print(json.dumps(post_to_dict(view.post), indent=2, sort_keys=True), "\n\n")
