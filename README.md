# BTCBot
A Discord BTC bot for listing price in various currencies and assets

# Install:

```pip install -r requirements.txt```

# Configure

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

>ANTI_BOT_SERVER_ID=Server on which to enable anti bot

>NEW_USER_MSG=Hello welcome to the server (OPTIONAL if ENABLE_ANTI_BOT=0)

>SALT1=a 2-5 digit numerical salt (OPTIONAL if ENABLE_ANTI_BOT=0)

>SALT2=a 5-9 digit numerical salt (OPTIONAL if ENABLE_ANTI_BOT=0)

>ERROR=An error message to return when the bot doesnt understand a DM. ex: Sorry, I didn't understand that.

>USER_ROLE=the role name of the role to apply to new users who complete anti-bot verification

>MOD_ROLE=the role name for mods of the server

>ENABLE_BAN_PATTERN=1 or 0 to enable or disable ban patterns

>BAN_PATTERN=regex pattern array matching auto-banned users

# Run
Once the `BOT_PREFIX` and `DISCORD_TOKEN` are configured, you can run the bot by executing the `btcbot.py` module.

#How to Contribute to the Discord Bot

Contributing to this Discord bot project is straightforward. Just follow these simple steps:

**Step 1: Install Git**
- Download and install Git Bash from [https://git-scm.com/downloads](https://git-scm.com/downloads) if you haven't already.

**Step 2: Create a GitHub Account**
- If you don't have a GitHub account, create one at [https://github.com/](https://github.com/).

**Step 3: Configure Git**
- After installing Git Bash, you need to configure your Git credentials. This helps in identifying the author of the commits you make.
- Open Git Bash and enter the following commands:
`git config --global user.name "Your Name"`
`git config --global user.email "YourGitHubEmail@example.com"`

- **Note for Anonymity:** If you prefer to stay anonymous, you can use any name. To keep your email private, use the no-reply email provided by GitHub.
- Go to your GitHub account, click your profile icon in the top right corner, and go to 'Settings'.
- Navigate to 'Emails' and copy your `@users.noreply.github.com` email.
- Use this email in the git config command for `user.email`.


Go to the https://github.com/buttersbtc/BTCBot page and **Fork the repository**. You can achieve this by pressing the Fork button. Once you have forked it, click your icon again in the top right corner and go to "your repository". Select the BTCBot, press the green button <> Code and copy the HTTPS URL.

**Step 4: Clone the Repository**
- Open Git Bash where you want to add the bot directory. The easiest way is to right-click in the folder and select "Git Bash Here".
- Now type: `git clone [URL you copied here]`

**Step 5: Edit the Code**
- Make the necessary changes or additions to the code in your local repository.

**Step 6: Prepare and Push Your Changes**
- Type `git status` into Git Bash to see what files you have changed. You can even do `git diff fileName` to see the changes in that particular file.
- Create your own branch by writing: `git branch yourBranchName`
- Switch to your branch with `git checkout yourBranchName`.
- Stage your changes with `git add fileName` (note: add the files you changed and want to push for review).
- Commit your changes with `git commit -m "add a short message here on what you did, try not to exceed 50 characters"`.
- Push your changes with `git push origin yourBranchName`.

**Step 7: Create a Pull Request**
- Go to your repository on GitHub. GitHub should suggest you can do a pull request (PR).
- Click on the suggestion to create a PR. If you'd like, give the PR a descriptive title and add a description.
- Submit the PR.

Congratulations, you have just completed your first pull request!
