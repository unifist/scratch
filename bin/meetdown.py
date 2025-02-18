#!/usr/bin/env python

import json
import zoom

client = zoom.Client()

for summary in client.meeting_summaries():
    print(json.dumps(client.meeting_summary(summary), indent=2, sort_keys=True))
