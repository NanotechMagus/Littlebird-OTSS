#!/usr/bin/python3.7

# Standard Library Imports
import discord
import logging, os, traceback, sys
from discord.ext import commands
import argparse

# Locally Developed Imports
from modules.lbinit import lbInit as base
from modules.lbdb import mongoLB as db

# Third Party Imports


def main():
    # Start with the splash screen because why not!
    splash()

    # Start the initialization process
    init = base()

    littlebird = commands.Bot(command_prefix=init.config['Discord']['PREFIX'],
                              description=init.config['Discord']['DESCRIPTION'])

    for extension in gather_extensions(init.basedir):
        try:
            littlebird.load_extension(extension)
        except Exception as err:
            logging.warning(f'Failed to load extension {extension}.')

    littlebird.run(token=init.config['Discord']['TOKEN'])

    return


def splash():
    print('Welcome to to the Littlebird Discord Bot!\n '
          'This bot was developed and Copyright © 2019 Magus Khunsehr on the FFXIV Balmung Server\n'
          'By using this program, you accept the LICENSE agreement located at the top level of the directory.\n\n'
          'Now that the crazy stuff is out of the way, let\'s begin!\n')
    return


def gather_extensions(basedir):

    cogsdir = os.path.join(basedir, "cogs")
    reglist = [f for f in os.listdir(cogsdir) if os.path.isfile(os.path.join(cogsdir, f))]
    splitlist = [os.path.splitext(x)[0] for x in reglist]

    return ["cogs." + x for x in splitlist]


if __name__ == "__main__":
    main()
