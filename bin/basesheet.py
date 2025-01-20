#!/usr/bin/env python
"""
Creates a blank sheet and shares with the outreach admins
"""

import outreach
import gsheets

outreach_config = outreach.config()

sheet = gsheets.connect().create("Outreach Source - Base")

for admin in outreach_config["admins"]:
    sheet.share(admin, perm_type='user', role='writer')
