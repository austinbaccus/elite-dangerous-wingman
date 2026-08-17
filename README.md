![Wingman](https://github.com/user-attachments/assets/84db643c-85f6-49ab-86ec-d66d3a8a0136)
<div align="center"><h1>Elite Dangerous: Wingman</h1></div>

Wingman is a voice-activated ship assistant for Elite Dangerous. Speak a command, and an SLM interprets your command and maps it to a ship action. It will then execute that command in-game. 

"Hit the lights", "Give me some light", "Let there be light" → `activate lights` → the AI turns your ship's lights on in-game


## AI Usage
- I used AI to make this. I'd guess around 90% of the code was made with Claude. I would design the architecture and stub out empty function headers and then tell the AI "go fill out that function". 
- AI didn't make any design choices. I treated the AI like it's an intern that's really good at solving interview-style coding questions but awful at thinking in a context greater than one function.
- No AI one-shotting involved ("Claude, make me an app that listens to voice commands for Elite Dangerous and, uhhh, btw make no mistakes").

Note: Don't share this on the Elite Dangerous subreddit. As of right now, their subreddit rules say that if AI was used to make a project in any capacity, you can't promote it on their subreddit. I like that rule, so I don't plan on breaking it.


## Pre-requisites
- You need to have a local AI server running
- Python needs to be installed

## How To Run
```
git clone https://github.com/austinbaccus/elite-dangerous-wingman.git
cd elite-dangerous-wingman
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Commands
- all power to shields
- all power to engines
- all power to weapons
- cut power to shields
- cut power to engines
- cut power to weapons
- re-distribute power
- target sub-system
- deploy chaff
- engaging silent running
- jettison cargo
- deploy cargo scoop
- retract cargo scoop
- deploy landing gear
- retract landing gear
- deploy fighters
- recall fighters
- order fighters to defend
- order fighters to follow
- activate lights
- deactivate lights
- activate night vision
- deactivate night vision
- engage (charge frame shift drive)
- activate shield cell
- deploy heat sink

## FAQ

### How long does the AI take to interpret what I say?
- 0.5 seconds on an Nvidia 2080 running `LFM2.5-8B-A1B-UD-IQ4_XS`.
- Loading a smaller model or using a faster GPU will lower the time it takes to interpret what you say.

### How do I run the AI
- Bring Your Own AI. 
- I run a `llama.cpp` server locally and I point the app at that. I run it on a separate machine so that I can use my gaming computer to play the game and not have to worry about running the AI.