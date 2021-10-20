# BTCBot
A Discord BTC bot for listing price in various currencies and assets

Create a new file named .env in the same directory as btcbot.py with the following contents:

>BOT_PREFIX=character-that-calls-bot, ex: !

>DISCORD_TOKEN=your-discord-bot-token

>REPORT_CHANNEL=your-channel-name-for-reports

>BLACKLIST=word1,website2,word3

>IMAGEONLY_CHANNEL=your-channel-name-for-images-only (OPTIONAL if ENABLE_IMAGEONLY=0)

>ENABLE_BLACKLIST=0 or 1, 1 is enabled. Enables word blacklist

>ENABLE_IMAGEONLY=0 or 1, 1 is enabled. Enables Image only enforcement in image channel

>ENABLE_REPORTS=0 or 1, 1 is enabled. Enables user reports to report channel

>ENABLE_EASTER_EGG=0 or 1, 1 is enabled. Enables posting of easter egg messages when triggered.

>EASTER_EGG_TRIGGER=keyword that triggers easter egg. (OPTIONAL if ENABLE_EASTER_EGG=0)

>EASTER_EGG_PERCENT_CHANCE=1-100 (OPTIONAL if ENABLE_EASTER_EGG=0)

>EASTER_EGG=Secret message to be played by bot when easter egg triggers (OPTIONAL if ENABLE_EASTER_EGG=0)

>ENABLE_ANTI_BOT=0 or 1, 1 is enabled. Enables anti-bot captcha and permissioned joining and role management. Users will need to complete a DM exchange with the bot to be applied a role which gives them permissions to use discord.

>NEW_USER_MSG=Hello welcome to the server (OPTIONAL if ENABLE_ANTI_BOT=0)

>SALT1=a 2-5 digit numerical salt (OPTIONAL if ENABLE_ANTI_BOT=0)

>SALT2=a 5-9 digit numerical salt (OPTIONAL if ENABLE_ANTI_BOT=0)

>ERROR=An error message to return when the bot doesnt understand a DM. ex: Sorry, I didn't understand that.

>USER_ROLE=the role name of the role to apply to new users who complete anti-bot verification

>MOD_ROLE=the role name for mods of the server