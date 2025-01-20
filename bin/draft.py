#!/usr/bin/env python

import json
import github

client = github.QL("unifist", "unum")

print(client.draft("Dude", "Sweet"))
