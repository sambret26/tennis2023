# -*- coding: utf-8 -*-

# IMPORTS
import sys
sys.path.append("modules")

import os
import discordTennis

# KEEPING ALIVE (en cas de deploiement sur replit)
if "Replit" in os.environ:
  import keep_alive
  keep_alive.keep_alive()

# START
discordTennis.main()
