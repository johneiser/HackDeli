#!/usr/bin/python

###################################################
#
#   HackDeli - written by Justin Ohneiser
# ------------------------------------------------
# This program will parse the accompanying XML
# file, HackDeliData.xml, displaying a menu of
# hacking options and their corresponding info.
#
# [Warning]:
# This script comes as-is with no promise of functionality or accuracy.  I strictly wrote it for personal use
# I have no plans to maintain updates, I did not write it to be efficient and in some cases you may find the
# functions may not produce the desired results so use at your own risk/discretion. I wrote this script to
# target machines in a lab environment so please only use it against systems for which you have permission!!
#-------------------------------------------------------------------------------------------------------------
# [Modification, Distribution, and Attribution]:
# You are free to modify and/or distribute this script as you wish.  I only ask that you maintain original
# author attribution and not attempt to sell it or incorporate it into any commercial offering (as if it's
# worth anything anyway :)
#
#   Format
# <types>
#   <type name="[type name]">
#       <area name="[area name]">
#           <option name="[option name]">
#               <info>[info]</info>
#           </option>
#       </area>>
#   </type>
# </types>
#
NAME = 'name'
FILE = 'hackdelidata.xml'
#
# Designed for use in Kali Linux 4.6.0-kali1-686
###################################################

import os, sys, copy
import xml.etree.ElementTree as ET

# ------------------------------------
# Toolbox
# ------------------------------------

def printLogo():
    os.system("clear")
    print """
====================================================================
        
888    888                   888      8888888b.           888 d8b
888    888                   888      888  "Y88b          888 Y8P
888    888                   888      888    888          888
8888888888  8888b.   .d8888b 888  888 888    888  .d88b.  888 888
888    888     "88b d88P"    888 .88P 888    888 d8P  Y8b 888 888
888    888 .d888888 888      888888K  888    888 88888888 888 888
888    888 888  888 Y88b.    888 "88b 888  .d88P Y8b.     888 888
888    888 "Y888888  "Y8888P 888  888 8888888P"   "Y8888  888 888
        
====================================================================
        """

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

def printHeader(stack):
    s = copy.deepcopy(stack)
    h = "-------"
    while not s.isEmpty():
        if s.peek().get(NAME):
            h = ("%s: %s\n" % (s.peek().tag, s.peek().get(NAME))) + h
        s.pop()
    print h

def printOptions(node):
    index = 0
    for i in node:
        index += 1
        if i.get(NAME):
            print ("%i:\t%s" % (index, i.get(NAME)))
        else:
            print (">\t%s" % (i.text))

def check(option):
    try:
        return int(option)
    except ValueError:
        return -1

# ------------------------------------
# Retrieve Data
# ------------------------------------

doc = None
try:
    doc = ET.parse(FILE)
except ET.ParseError as e:
    print("[!] Unable to parse XML file: %s\n%s" % (FILE, e))
    sys.exit()
except IOError:
    print("[!] Can't find %s, must be local to execute" % FILE)
    sys.exit()

# ------------------------------------
# Process Data
# ------------------------------------

try:
    s=Stack()
    s.push(doc.getroot())
    
    while not s.isEmpty():
        printLogo()
        printHeader(s)
        printOptions(s.peek())
        choice = check(raw_input("\n0:\tBack\n\n>>> "))
        if choice < 0:
            continue
        elif choice == 0:
            s.pop()
        elif choice <= len(s.peek()):
            if s.peek()[choice - 1].get(NAME):
                s.push(s.peek()[choice - 1])
            else:
                continue
        else:
            continue
except Exception as e:
    print("[!] An error has occurred: %s" % e)
    sys.exit()
except KeyboardInterrupt:
    print("\nExiting")
    sys.exit()

