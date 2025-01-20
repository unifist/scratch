#!/usr/bin/env python

import outreach
import gsheets

gspread_client= gsheets.connect()
outreach_config = outreach.config()

gspread_client.copy("1fKKusiFSjjDmfl-z8hrBfEgqEZCnSwTPEighMEN_0vY", title=f"Outreach Source - {outreach_config['link']}")

sheet = gspread_client.open(f"Outreach Source - {outreach_config['link']}")

for admin in outreach_config["admins"]:
    sheet.share(admin, perm_type='user', role='writer')
