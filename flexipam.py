#!/usr/bin/env python3

import sys
import getopt

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

_debug = False

flexipam_config = "/home/lechner/Projects/PAM/flexipam/sample-config/"

def GetFirstChild(e): return e[0] if len(e) else None

def execute(which):
    if(_debug):
        print("Exec:\t", which)

    tree = ET.ElementTree(file=flexipam_config + "actions/" + which)
    action = tree.getroot()

    helper = action.find("helper")
    config = action.find("config")
    print("Call:\t", helper.text, "[" + config.text + "]")

def include(which):
    if(_debug):
        print("Load:\t", which)
        
    tree = ET.ElementTree(file=flexipam_config + "modules/" + which)
    module = tree.getroot()

    for part in module:
        eval(part)

    return True

def all(parts):
    for part in parts:
        if eval(part) == False:
            return False
    return True

def any(parts):
    for part in parts:
        if eval(part) == True:
            return True
    return False

def eval(part):
    if (_debug):
        print("Eval:\t", part.tag)

    if part.tag == "all":
        return all(part)
    
    elif part.tag == "any":
        return any(part)
    
    elif part.tag == "include":
        return include(part.text)

    elif part.tag == "execute":
        return execute(part.text)

    return False

def main(argv):                         
    try:                                
        opts, args = getopt.getopt(argv, "hp:d", ["help", "grammar="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = True
        elif opt in ("-p", "--protocol"):
            protocol_arg = arg

    tree = ET.ElementTree(file=flexipam_config + "protocols/" + protocol_arg)
    protocol = tree.getroot()

    for stage in protocol:
        print("\nOpen:\t", stage.tag)
        eval(GetFirstChild(stage))
        print("Close:\t", stage.tag)

        
if __name__ == "__main__":
    main(sys.argv[1:])
