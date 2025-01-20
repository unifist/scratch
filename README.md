unum/scratch
============

This has a bunch of fun little scripts to do shit.

This is a world of and for self starters. Be so. Forgiveness over Permission.

Right now, only know how to do on Mac/Linux. Happy to learn otherwise or work with folks but need thigns simple.

There's infinite ways to do stuff. This is the way I do stuff and thus the best way I can currently help you.

# accounts

You don't have to use your personal accounts for anything. These accounts are needed to join us in developing: And they all sould be free:
- [Gmail](https://support.google.com/mail/answer/56256?hl=en)
  - (Unifist Unum Group)[https://groups.google.com/g/unifist-unum/]
- [GitHub](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)
  - [2FA](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication)
  - [SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [BlueSky](https://support.bluesky.com/hc/en-us/articles/24779732343955-How-do-I-create-an-account-on-BlueSky-com)
- [Discord](https://support.discord.com/hc/en-us/articles/360033931551-Getting-Started)

# install

Install on your Mac:
- Apple Xcode: https://developer.apple.com/xcode/
- Homebrew: https://brew.sh/
- VS Code: https://code.visualstudio.com/
- GitHub Desktop: https://desktop.github.com/download/
- Docker Desktop: https://docs.docker.com/desktop/

# repo

Checkout this Repo using the GitHub Desktop option and make sure you can open it in VSCode with ctl-cmd-a.

Ask Gaf for a copy of the secrest zip and he'll share it with via 1Pass. Put the file in this directory here.

GUARD THESE FILES WITH YOUR LIFE.

Hit ctrl-~ to open a shell.

# make

We use make to do stuff. It's just an ancient process for writing code that works well.

Lots of these commands we need have lots of complicated options. With make we're able to bundle all that up and turn all those options into simple commands.

Much like we're trying to do with Unifist, the goal is to take a million possibilities and ways to do things, and boil them down into a handful of simple predictable process.

Check out [Makefile](Makefile) for more

## secret

To install the secrets, copy into the dir and from the shell:

`make unzip`

This sets up all teh secrets for the code to work.

## build

`make build`

Creates the Docker image. Check out [Dockerfile](Dockerfile) for more

## shell

`make shell`

Runs and jumps into the running Docker image. Use this to poke around and debug.

## MOAR

There's a lot more in there. Check them out to see what they do! You're a developer now!
