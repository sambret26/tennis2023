import os
# -*- coding: utf-8 -*-

# IMPORTS
import sys
import export
sys.path.append("modules")

import discordTennis

# KEEPING ALIVE (en cas de deploiement sur replit)
if "Replit" in os.environ:
  import keep_alive
  keep_alive.keep_alive()

# START
discordTennis.main()
export.main()
