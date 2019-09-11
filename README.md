# FlightGearBrasil's Discord Bot

[![Build Status](https://img.shields.io/badge/heroku-deployed-brightgreen?logo=heroku)](https://travis-ci.com/flightgearbrasil/fgbr-discord-bot-py) [![Build Status](https://img.shields.io/travis/com/flightgearbrasil/fgbr-discord-bot-py?logo=travis)](https://travis-ci.com/flightgearbrasil/fgbr-discord-bot-py) [![GNU General Public License](https://img.shields.io/github/license/flightgearbrasil/fgbr-discord-bot-py?logo=github)](http://www.gnu.org/licenses/gpl-3.0.en.html)

## Manual deploy and run

- Required Python 3.7.3
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

Working with Discord API 1.0.1
