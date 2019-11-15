# Bauwens Skills

## Git Setup

Install git: https://git-scm.com/download/win

First clone this repository
git clone https://github.com/rbauwens/BauwensSkills.git
This will create a folder called BauwensSkills wherever you run it from

## Setup for the ASK CLI

Basically we're just following https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html
Watch the video - it helps

### Install Node
1. Go to https://nodejs.org/en/download/
2. Click to download the windows installer msi file - the LTS version
3. Open the file to start the installer

Note: I used all the defaults and checked the box to include extra things like Chocolatey
Once the node installation finished it popped up a cmd line windows to install all the extras. 
possibly this is not necessary. if someone tries without please update this Readme

### Install ASK

Run these:
npm install -g --production windows-build-tools
npm install -g ask-cli
ask init

ask init will make you log into an amazon developer account. 

## Clone the Capital Adventure project
This should be a one time operation.
From the BauwensSkills folder run
ask clone -s amzn1.ask.skill.b0a231a3-32f1-4aff-bad4-c72eb69a149c

This will download the skill as you see it on the developer console
Now the setup is kind of weird because the Alexa stuff comes with it's own source control.
i.e. BauwensSkills is one git repository and Captial_Adventure is another one within in.

If you do "git log" in the Capital_Adventure folder then you will see the history of changes made on the developer console.

Have a read of this to understand what's going on within the Captial_Adventure folder
https://developer.amazon.com/blogs/alexa/post/8a602054-6ba8-4b6e-b298-c4811840e680/using-the-alexa-skills-kit-command-line-interface-with-alexa-hosted-skills

Every time we deploy we will be overwriting Capital_Adventure/master with our own changes
I don't see a way round that yet.

## Deploy Capital Adventure

Make sure you're in the BauwensSkills/Captial_Adventure folder
Run 
ask deploy

This will give you the URL of where you can view and interact with the skill in the Amazon developer console.
If you go to the test tab then you can start by saying "Open Capital Adventure"

