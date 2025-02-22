#!/usr/bin/env python

import json
import bsky

client, profile = bsky.connect()

print('Welcome,', profile.handle)

followers = client.get_followers(actor=profile.handle)

for follower in followers.followers:
    print(follower.handle)


post_objects = client.get_author_feed(actor=profile.handle, limit=3).feed
posts = []
for post in post_objects:
    record = post.post.record
    subject = getattr(record, "subject", None)

    replies = client.get_post_thread(uri=post.post.uri).thread.replies

    for reply in replies:
        print(f"Reply: {reply.post.record.text}")



"""


    print(
        {
            "uri": post.post.uri,
            "did": post.post.author.did,
            "created_at": record.created_at,
            "root_uri": reply.root.uri if reply else None,
            "parent_uri": reply.parent.uri if reply else None,
            "subject_uri": subject.uri if subject else None,
            "card_link": getattr(record, "external_uri", None),
            "like_count": post.post.like_count,
            "reply_count": post.post.reply_count,
            "repost_count": post.post.repost_count,
            "labels": post.post.author.labels,
            "text": record.text,
            # "images": record.embed. if record.embed else [],
        }
    )

response = client.app.bsky.feed.get_author_feed(params={
    "actor": "gaf3.com",
    "limit": 5,
    "filter": "posts_with_replies"
})

for view in response.feed:

    print(view.post)

    if hasattr(view.post.record, "reply"):
        print(view.post.record.reply)

        print(view.post.record.reply.parent.uri)

        client.get_post(
            uri=view.post.record.reply.parent.uri,
        )

        response = client.get_likes(
            uri=view.post.uri,
            limit=10
        )

    for like in response.likes:
        print(like.actor.handle)


"""
