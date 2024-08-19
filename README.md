# SoC Discord Bot / Taair

A discord bot providing detailed information and insights about the game Sword of Convallaria, directly based on in-game data.
It's fully privacy-friendly — using only slash commands and never tracking any user data.

[Install Link](https://discord.com/oauth2/authorize?client_id=1267190340494954508)

## Config

Following files have to be modified to deploy the bot correctly:
- ``soc_discord_bot/commands/icons.py`` - contains mappings for icons to emoji

## Commands

### /soc unit name:

Shows the general information about a unit, and offers my detailed information using buttons.
This command is implemented in ``soc_discord_bot/commands/unit.py``


### /soc gacha

Shows all current and future banners that can be found in the data.
This command is implemented in ``soc_discord_bot/commands/gacha.py``


### /update_db

Updates the database of the bot.
This command is implemented in ``soc_discord_bot/bot.py``.
The command is only available for the bot owner.