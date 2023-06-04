# Overview

WIP port of [my high school senior project](https://github.com/slaugaus/bullet-heck) from [Pygame](https://www.pygame.org/) to [Arcade](https://arcade.academy).

I wanted to come back to my largest-to-date coding project and apply my additional 5 years of knowledge to it. I've been meaning to do it in a "real" game engine, but this will suffice for now.

[Software Demo Video](https://www.youtube.com/watch?v=hVQwVYYdkds)

### How to Play
* Run BulletHeck.py in the data folder. I'll eventually hook up the launcher and compile binaries.
* Kill enemies to get points! ~~Collect powerups!~~ Don't get hit!
* If you get stuck while moving, you're holding down too many buttons. Try pressing the autofire button.

|Keyboard|Action|
|--|--|
|Arrow keys|Move the ship|
|Z or Spacebar|Hold to fire bullets|
|A|Press to toggle firing bullets automatically|
|Z or Spacebar (with autofire on)|Don't fire bullets|


# Development Environment

IDE: VS Code with a bunch of extensions, including the recommended Python ones.

Game graphics were made by 18-year-old me in [Blender](https://blender.org) and rendered to individual PNGs. I used [ImageMagick](https://imagemagick.org) to convert them to spritesheets.

Sound effects obtained from https://www.zapsplat.com  
Font used (in BH Classic and eventually this) is "Uno Estado" by Dan Zadorozny (Iconian Fonts)

"Space Fighter Loop"  
Kevin MacLeod (incompetech.com)  
Licensed under Creative Commons: By Attribution 3.0  
http://creativecommons.org/licenses/by/3.0/

Language: Python 3.10+ (`match()` is used) with Arcade 2.6.17 and some of the built-in libraries

# Useful Websites

* [Arcade documentation and tutorials](https://arcade.academy)
* ["Create a spritesheet quick and easy with imagemagick" by vollnixx](https://vollnixx.wordpress.com/2012/08/25/create-a-spritesheet-quick-and-easy-with-imagemagick/)
* [The original Bullet Heck, I guess?](https://github.com/slaugaus/bullet-heck)

# Future Work

* A bunch of stuff.
* Proper GUI
* Player health and/or lives
* Health pickups and powerups
* Enemies don't fire bullets
* A balance pass?
* More that I can't think of right now