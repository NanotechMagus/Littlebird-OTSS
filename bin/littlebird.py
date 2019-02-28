#!/usr/bin/python3.7

# Standard Library Imports
import discord
import logging, os, traceback, sys
from discord.ext import commands
import argparse

# Locally Developed Imports
from modules import lbinit

# Third Party Imports


def main():
    # Start with the splash screen because why not!
    splash()

    # Get arguments from sysarg, apply them as necessary
    # Should I move the sys.args to initialize, or is that too many layers in?

    lbinit.initialize()
    return


def initialize():
    # Lets take some system args and process them
    parser = argparse.ArgumentParser()
    parser.add_argument("rb", "--rebuild", help="Rebuild the Bot using settings from littlebird.ini")
    parser.add_argument("v", "--verbosity", action="count", help="Set initial verbosity")
    args = parser.parse_args()

    lbinit.logwrapper(args.verbosity)

    if args.rebuild:
        try:
            lbinit.firstrun(os.path.dirname(os.path.abspath(__file__)))
        except Exception as err:
            logging.warn(f'Rebuild Error: {err}')
            lbinit.cleanexit(err.args)

    return


def splash():
    print('Welcome to to the Littlebird Discord Bot!\n '
          'This bot was developed and Copyright © 2019 Magus Khunsehr on the FFXIV Balmung Server\n'
          'By using this program, you accept the LICENSE agreement located at the top level of the directory.\n\n'
          'Now that the crazy stuff is out of the way, let\'s begin!\n')
    return


if __name__ == "__main__":
    main()
