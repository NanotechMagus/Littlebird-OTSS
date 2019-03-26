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
    lbdb = db(init.config["MongoDB"])

    return


def splash():
    print('Welcome to to the Littlebird Discord Bot!\n '
          'This bot was developed and Copyright © 2019 Magus Khunsehr on the FFXIV Balmung Server\n'
          'By using this program, you accept the LICENSE agreement located at the top level of the directory.\n\n'
          'Now that the crazy stuff is out of the way, let\'s begin!\n')
    return


if __name__ == "__main__":
    main()
