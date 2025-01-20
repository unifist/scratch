#!/usr/bin/env python

import atproto
import bsky

client, profile = bsky.connect()

print('Welcome,', profile.display_name)

post = client.send_post("Dope")
client.like(post.cid)
