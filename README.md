# elite-dangerous-wingman

## What is this?
Voice-activated ship assistant for Elite Dangerous. 

You speak a command. Speech-to-text turns that into text. The text is sent to a small AI interpreter that maps what you said to one of 26 in-game commands. A virtual key corresponding to that command is pressed, which executes the command inside Elite Dangerous.

You need to have Ollama running on your machine. 

## Installation
1. Create or start an Ollama server on your machine
2. `ollama create qwen-cmd -f m`
3. `pip install {anything that's missing}`
4. `python main.py`

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
### Why does the first command take so long to be interpreted?
- Because Ollama needs to load the model, which takes a minute or two.
- You can pre-load the model in Ollama to reduce the time it takes to load. Or, while the game is booting up, say a fake command to get it started.

### How long does the AI take to interpret what I say?
- 3.7 seconds on an Nvidia 3060.
- Loading a smaller model or using a faster GPU will lower the time it takes to interpret what you say.

### How much VRAM does this use?
- ~5 GB.
- If you need to lower the VRAM usage, swap out the default model (`qwen2.5:7b-instruct-q5_K_M`) with something like Qwen2.5-0.5B. It will not be as accurate when it interprets your commands though.
