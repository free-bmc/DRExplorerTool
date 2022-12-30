#!/usr/bin/env python3
#MIT License

#Copyright (c) 2022 hramacha

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


from redfish_cli import DRSetup
from redfish_cli import CLIStart

ToolVersion = "1.0"

def main():
    print("Welcome to DMTF Redfish Explorer Utility")
    print("The Tool that allows to Explore DMTF Redfish and Swordfish Schema bundles ")
    print("The tool parses through the Schema bundle from ServiceRoot.json and connects them together")
    print("")
    print("The tool features :")
    print(" 1. Check the DMTF Redfish and Swordfish and get the list of available Schema Bundles to download ")
    print(" 2. Download the DMTF Redfish and Swordfish Schema bundles")
    print(" 3. Load and Explore the Schemas and get more information")
    print(" 4. CLI that supports exploration")

    DRSetup()
    CLIStart(ToolVersion)

if __name__ == "__main__":
    main()
