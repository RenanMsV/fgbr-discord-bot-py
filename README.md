# FlightGearBrasil's Discord Bot

## Manual deploy and run

- Required Python 3.6.8+
- Make a virtual environment with ```python -m venv venv```
- Enable the virtual environment mode with ```call ./venv/scripts/activate``` for windows or ```source ./venv/bin/activate``` for linux
- Install dependencies with ```pip install -r requirements.txt```
- Setup the environment variables, 3 are needed:
  - BOT_TOKEN (Discord's bot secret token) 
  - BOT_AIS_KEY (AISWEB API key)
  - BOT_AIS_TOKEN (AISWEB API pass)
- Here you can see how to use and request your [Discord's bot token](https://discordapp.com/developers/applications/)
- Here you can see how to use and request your [AISWEB API key](https://documenter.getpostman.com/view/6803747/S17wMRAF?version=latest)
- Start the bot with ```python bot.py``` or ```python3 bot.py```

## You can also automatically deploy and host for free with <heroku.com>

Working with Discord API 0.16.12
