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

#Main Menu 
#    Load Schema From DMTF 
#    Load Schema From Disk 

#Schema Main Menu
#    Info 
#    Uri Map 
#    Schema Version Map 
#    States & Option Map     
#    Search Definitions
#    Search Properties
#    Search Enums 

#Schema File Menu 
#    Info 
#    Definitions 
#    Properties
#    Enums 

import os
import json
import requests, zipfile, io

from urllib.request import urlopen

from redfishSchema import RedfishSchemaBuildClass
from redfishSchema import SchemaInfoClass
from redfishSchema import SchemaDownloadClass
from redfishSchema import SchemaLoadClass


RedfishSchemaBuildList = []
CurrentSchemaLoad = None

DRSchemaLoadList = []

LocalRedfishSchemaSelected = None
LocalSwordfishSchemaSelected = None
LocalRedfishDirectory = None
LocalSwordfishDirectory = None

DMTFRedfishSchemaInfoList = []
DMTFSwordfishSchemaInfoList = []

DMTFRedfishSchemaDownloadList = []
DMTFSwordfishSchemaDownloadList = []

DMTFRedfishSchemaLoadList = []
DMTFSwordfishSchemaLoadList = []

DRRedfishBasePath = None
DRSwordfishBasePath = None
SetupComplete = False
IncludeSwordfishSchemas = False
DRBasePath = None

def DRSetup():
    global DRBasePath    
    global DRRedfishBasePath    
    global DRSwordfishBasePath    

    DRBasePath = os.path.expanduser('~')+"/DRExplorerHome"
    DRRedfishBasePath = os.path.expanduser('~')+"/DRExplorerHome/RedfishSchemas"
    DRSwordfishBasePath = os.path.expanduser('~')+"/DRExplorerHome/SwordfishSchemas"

    print("\n\nSetup In Progress...")
    if os.path.exists(DRBasePath) == False:
        print("First Time Setup ... ")
        print("Please be patient will take few minutes to set up...")
        os.mkdir(DRBasePath)
        os.makedirs(DRRedfishBasePath)
        os.makedirs(DRSwordfishBasePath)
        print("Scanning for DMTF Redfish Schema Bundles ...", end=" ")
        urlfile = urlopen("https://dmtf.org/dsp/DSP8010")
        dsp8010url = urlfile.read().decode(urlfile.headers.get_content_charset())
        lines = dsp8010url.splitlines(True)
        schema_json_list = []
        count = 1
        for line in lines:
            if "DSP8010_" in line:
                schema_json = {}
                urlstring = line.split("\"")[1]
                schemaname = urlstring.split("/")[len(urlstring.split("/")) -1].replace(".zip","")
                scut = "rf"+str(count)
                count += 1
                dmtfschema = SchemaInfoClass(schemaname, urlstring, scut)
                schema_json['SchemaName'] = schemaname.strip()
                schema_json['URL'] = urlstring.strip()
                schema_json['Shortcut'] = scut
                schema_json_list.append(schema_json)
                DMTFRedfishSchemaInfoList.append(dmtfschema)
        print("Found ", len(DMTFRedfishSchemaInfoList))
        data = {}
        data['SchemaGroup'] = "Redfish"
        data['SchemaList'] = schema_json_list
        PrettyJson = json.dumps(data, indent=4, separators=(',',':'))
        with open(os.path.join(DRRedfishBasePath,"SchemaList.json"), "w") as outfile:
            outfile.write(PrettyJson)        
        outfile.close()        
        urlfile.close()

        print("Scanning for DMTF Swordfish Schema Bundles ...", end=" ")         
        urlfile = urlopen("https://www.snia.org/forums/smi/swordfish")
        swordfishurl = urlfile.read().decode(urlfile.headers.get_content_charset())
        lines = swordfishurl.splitlines(True)
        schema_json_list.clear()
        count = 1
        for line in lines:
            if "_Schema.zip" in line:
                schema_json = {}
                urlstring = line.split("\"")[1]
                schemaname = urlstring.split("/")[len(urlstring.split("/")) -1].replace(".zip","")
                scut = "sf"+str(count)
                count += 1
                swordfishschema = SchemaInfoClass(schemaname, urlstring, scut)
                schema_json['SchemaName'] = schemaname.strip()
                schema_json['URL'] = urlstring.strip()
                schema_json['Shortcut'] = scut
                schema_json_list.append(schema_json)
                DMTFSwordfishSchemaInfoList.append(swordfishschema)            
        print("Found ", len(DMTFSwordfishSchemaInfoList))
        data = {}
        data['SchemaGroup'] = "Swordfish"
        data['SchemaList'] = schema_json_list
        PrettyJson = json.dumps(data, indent=4, separators=(',',':'))
        with open(os.path.join(DRSwordfishBasePath,"SchemaList.json"), "w") as outfile:
            outfile.write(PrettyJson)        
        outfile.close()        
        urlfile.close()
    else:
        print("Scanning for DMTF Redfish Schema Bundles ...", end=" ")
        json_file = open(os.path.join(DRRedfishBasePath,"SchemaList.json"), "r")
        dataJson = json.load(json_file)
        schema_list_data = dataJson['SchemaList']
        for index in range(0,len(schema_list_data)):
            schemadata = schema_list_data[index]
            dmtfschema = SchemaInfoClass(schemadata.get("SchemaName"), schemadata.get("URL"), schemadata.get("Shortcut"))
            DMTFRedfishSchemaInfoList.append(dmtfschema)
        json_file.close()
        print("Found ", len(DMTFRedfishSchemaInfoList))

        print("Scanning for DMTF Swordfish Schema Bundles ...", end=" ")         
        json_file = open(os.path.join(DRSwordfishBasePath,"SchemaList.json"), "r")
        dataJson = json.load(json_file)
        schema_list_data = dataJson['SchemaList']
        for index in range(0,len(schema_list_data)):
            schemadata = schema_list_data[index]
            dmtfschema = SchemaInfoClass(schemadata.get("SchemaName"), schemadata.get("URL"), schemadata.get("Shortcut"))
            DMTFSwordfishSchemaInfoList.append(dmtfschema)
        json_file.close()
        print("Found ", len(DMTFSwordfishSchemaInfoList))

    print("Setup Complete, Ready to Explore ...")

def DRDownload(downloadchoice):
    downloadlist = []
    if "," in downloadchoice:
        dlist = downloadchoice.split(',')
        for dl in dlist:
            downloadlist.append(dl.strip())
    else:
        downloadlist.append(downloadchoice)

    for dl in downloadlist:
        if dl.strip().startswith("rf"):
            for sdata in DMTFRedfishSchemaInfoList:
                if sdata.ShortCut == dl.strip():
                    if os.path.exists(DRRedfishBasePath+"/"+sdata.schemaName) == True:
                        print("Already Uploaded ", sdata.schemaName, "From ", sdata.URL)    
                        continue
                    os.mkdir(DRRedfishBasePath+"/"+sdata.schemaName)
                    print("Retriving ", sdata.schemaName, "From ", sdata.URL)
                    r = requests.get(sdata.URL)
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    z.extractall(DRRedfishBasePath+"/"+sdata.schemaName) 
                    ScanDMTFSchemas()
        elif dl.strip().startswith("sf"):
            for sdata in DMTFSwordfishSchemaInfoList:
                if sdata.ShortCut == dl.strip():
                    if os.path.exists(DRSwordfishBasePath+"/"+sdata.schemaName) == True:
                        print("Already Uploaded ", sdata.schemaName, "From ", sdata.URL)    
                        continue
                    os.mkdir(DRSwordfishBasePath+"/"+sdata.schemaName)
                    print("Retriving ", sdata.schemaName, "From ", sdata.URL)
                    r = requests.get(sdata.URL)
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    z.extractall(DRSwordfishBasePath+"/"+sdata.schemaName) 
                    ScanDMTFSchemas()                        

def ScanDMTFSchemas():
    DMTFRedfishSchemaDownloadList.clear()
    DMTFSwordfishSchemaDownloadList.clear()
    obj = os.scandir(DRRedfishBasePath)
    for entry in obj:
        if entry.is_dir():
            for sdata in DMTFRedfishSchemaInfoList:
                if entry.name in sdata.URL:
                    sdc = SchemaDownloadClass(DRRedfishBasePath,sdata, entry)
                    DMTFRedfishSchemaDownloadList.append(sdc)                    
    
    obj = os.scandir(DRSwordfishBasePath)
    for entry in obj:
        if entry.is_dir():
            for sdata in DMTFSwordfishSchemaInfoList:
                if entry.name in sdata.URL:
                    sdc = SchemaDownloadClass(DRSwordfishBasePath,sdata, entry)
                    DMTFSwordfishSchemaDownloadList.append(sdc)

def DRLoadSchemaBundle(id):
    global CurrentSchemaLoad
    global RedfishSchemaDB
    global DRSchemaLoadList

    if id == None:
        print("ID\tRedfish Schema  \t Swordfish Schema")
        for slc in DRSchemaLoadList:
            print(slc.lname,"\t",slc.RedfishSDC.sdata.schemaName,"\t", slc.SwordfishSDC.sdata.schemaName)
        return
    
    if id != "schema":
        if len(DRSchemaLoadList) != 0:        
            for slc in DRSchemaLoadList:
                if id == slc.lname:
                    CurrentSchemaLoad = slc
                    print("ID ", slc.lname," is Loaded")
        else:
            print("ID Not found... Load List Empty")
            return
        return

    # Load from the Download List      
    ScanDMTFSchemas()

    if len(DMTFRedfishSchemaDownloadList) == 0:
        print("No Redfish Schemas Downloaded")
        return

    print("Redfish Schemas Download List: ")
    print("\tID\tSchema Name",)
    for sdc in DMTFRedfishSchemaDownloadList: 
        print("\t",sdc.sdata.ShortCut,"\t", sdc.sdata.schemaName)
    RedfishSchemaSelected = input("Select Schema (use ID): ")
    RedfishSchemaSelected = RedfishSchemaSelected.strip()
    user_info_validated = False
    for sdc in DMTFRedfishSchemaDownloadList: 
        if sdc.sdata.ShortCut == RedfishSchemaSelected:
            user_info_validated = True
            RedfishSchemaInfoSelected = sdc
            break
    if user_info_validated == False:
        print("Incorrect Schema ID selected ")
        return

    print("Swordfish Schemas Download List: ")
    print("\tID\tSchema Name",)
    for sdc in DMTFSwordfishSchemaDownloadList: 
        print("\t",sdc.sdata.ShortCut,"\t", sdc.sdata.schemaName)
    SwordfishSchemaSelected = input("Select Schema (use ID): ")
    SwordfishSchemaSelected = SwordfishSchemaSelected.strip()
    user_info_validated = False
    for sdc in DMTFSwordfishSchemaDownloadList: 
        if sdc.sdata.ShortCut == SwordfishSchemaSelected:
            user_info_validated = True
            SwordfishSchemaInfoSelected = sdc
            break
    if user_info_validated == False:
        print("Incorrect Schema ID selected ")
        return

    user_name = "" 
    while len(user_name) == 0: 
        user_name = input("Select a unique ID for this Load Combination: ")
        if len(user_name) != 0: 
            break

    
    LocalRedfishDirectory = os.path.abspath(RedfishSchemaInfoSelected.fentry)+"/json-schema"
    LocalSwordfishDirectory = os.path.abspath(SwordfishSchemaInfoSelected.fentry)+"/json-schema"    
    CurrentSchemaBuild = RedfishSchemaBuildClass("Disk", LocalRedfishDirectory, LocalSwordfishDirectory)    
    RedfishSchemaDB = CurrentSchemaBuild.RedfishSchemaDB
    CurrentSchemaBuild.LoadSchemaFromDMTF = False
    CurrentSchemaBuild.RedfishSchemaBuild()
    
    schema_load = SchemaLoadClass(user_name, RedfishSchemaInfoSelected, SwordfishSchemaInfoSelected, CurrentSchemaBuild)
    DRSchemaLoadList.append(schema_load)
    CurrentSchemaLoad = schema_load
    print("Schema Loaded and Ready for exploration")

def PrintCurrentSchemaInfo():
    RedfishSchemaDB = CurrentSchemaLoad.SchemaBuild.RedfishSchemaDB

    if CurrentSchemaLoad.SchemaBuild.LoadSchemaFromDMTF == True: 
        print("\t Schema Bundle Location : Online")
    else:
        print("\t Redfish Schema Bundle Location : ", CurrentSchemaLoad.SchemaBuild.LocalRedfishDirectory)
        if IncludeSwordfishSchemas == True:
            print("\t Swordfish Schema Bundle Location : ", CurrentSchemaLoad.SchemaBuild.LocalSwordfishDirectory)
    if CurrentSchemaLoad.SchemaBuild.SchemaBundleVersion != None:        
        print("\t Schema Bundle Version                : ", CurrentSchemaLoad.SchemaBuild.SchemaBundleVersion)
    else: 
        print("\t Schema Bundle Version                : ", RedfishSchemaDB.RedfishServiceRoot.Header.release)
    
    print("\t Total Schemas Parsed                 : ", len(RedfishSchemaDB.RedfishSchemaList))
    print("\t Total Schemas Definitions Found      : ", len(RedfishSchemaDB.DefinitionsDB))
    print("\t Total Schemas Properties Found       : ", len(RedfishSchemaDB.PropertiesListDB))
    print("\t Total Schemas Options/Enums Found    : ", len(RedfishSchemaDB.OptionsDB))

def PrintURIMap():
    CurrentSchemaLoad.SchemaBuild.RedfishSchemaDB.UriURLLayout.PrintUri()    

def CLIStart(ToolVersion):
    global CurrentSchemaLoad
    CurrentSchemaName = None
    CurrentSchemaVersion = None

    print("CLI started ...")    
    while True:
        option = input("RSE CLI >> ")
        #print(option)
        if option == "quit":
            exit()
        elif option == "help":
            print("Commands and Options:")
            print("\tversion       <options>                Version Info ")
            print("\trflist                                 List DMTF Redfish Schema Bundle ")
            print("\tsflist                                 List DMTF Swordfish Schema Bundle ")
            print("\tdownload                               Download Schema Bundle")            
            print("\tload [ ,schema,<ID>]                   Load Redfish Schema Bundle Options ")
            print("\t                                       No Arg - List Loaded Schema Bundle  ")
            print("\t                                       schema - Loaded a Schema Bundle      ")
            print("\t                                       <ID> -   Loaded Schema Bundle with ID ")
            print("")
            print("\tsb <options>                           Schema Bundle Options")
            print("\t                                       No Arg                  - Display Current Schema Bundle ")
            print("\t                                       set <ID>                - Set the Schema Bundle ")            
            print("\t                                       info                    - Schema Bundle info ")
            print("\t                                       urimap                  - URI Map ")
            print("\t                                       list schemas            - List Schemas   ")
            print("\t                                       list versions <schema>  - List Schema Versions ")            
            print("")
            print("\tsc <options>                           Schema Options")
            print("\t                                       No Arg                  - Display Current Schema, Version ")
            print("\t                                       set <Schema> <Version   - Set the Schema and Version")
            print("\t                                       info                    - Schema info ")
        
        elif option.startswith("version"):
            suboption = option.split(" ")
            if len(suboption) == 1 or suboption[1] == "help":         
                print("Version Options:")
                print("\ttool               Tool Version ")
            elif suboption[1] == "tool":
                print(ToolVersion)

        elif option.startswith("rflist"):
            print("Available DMTF Redfish Schema List ")
            for schemadata in DMTFRedfishSchemaInfoList:
                print(schemadata.ShortCut,"\t",schemadata.schemaName,"\t",schemadata.URL)
        
        elif option.startswith("sflist"):
            print("Available DMTF Swordfish Schema List ")
            for schemadata in DMTFSwordfishSchemaInfoList:
                print(schemadata.ShortCut,"\t",schemadata.schemaName,"\t",schemadata.URL)
        
        elif option.startswith("download"):
            ScanDMTFSchemas()
            print("ID\tSchema Name\t\tSchema Type")
            for sdc in DMTFRedfishSchemaDownloadList:
                print(sdc.sdata.ShortCut,"\t",sdc.sdata.schemaName,"\t Redfish")
            for sdc in DMTFSwordfishSchemaDownloadList:
                print(sdc.sdata.ShortCut,"\t",sdc.sdata.schemaName,"\t Swordfish")
            choice = input("Do you want to continue to Download Y/N ")
            if choice == "N":
                continue
            shortcutchoice = input("Choose one or more shortcuts to download, use , for multiple downloads ")
            DRDownload(shortcutchoice)
        
        elif option.startswith("load"):
            suboption = option.split(" ")
            if len(suboption) == 1:
                DRLoadSchemaBundle(None)
            if len(suboption) == 2:
                if suboption[1] == "schema":
                    DRLoadSchemaBundle("schema")
                else:
                    DRLoadSchemaBundle(suboption[1])

        elif option.startswith("sb "):            
            suboption = option.split(" ")
            if len(suboption) == 1:
                DRLoadSchemaBundle(None)
                print("Current Schema Bundle Information ")
                print("ID: ", CurrentSchemaLoad.lname, "\tRedfish Schema: ", CurrentSchemaLoad.RedfishSDC.sdata.schemaName,"\tSwordfish Schema: ", CurrentSchemaLoad.SwordfishSDC.sdata.schemaName)
                continue
            elif len(suboption) == 2:
                if suboption[1] == "info":
                    PrintCurrentSchemaInfo()
                elif suboption[1] == "urimap":
                    PrintURIMap()
            elif len(suboption) == 3:
                if suboption[1] == "list":
                    if suboption[2] == "schemas":
                        schema_types_list = []
                        print("Listing Schemas in the Bundle")
                        for rp in CurrentSchemaLoad.SchemaBuild.RedfishSchemaDB.OptionsDB:
                            schemaPrefix = rp.SchemaData.schemaName.split(".")[0]
                            if rp.key != schemaPrefix: 
                                continue
                            schema_types_list.append(schemaPrefix)

                        count = 0
                        print("Total Valid Schemas Found in the Schema Bundle :", len(schema_types_list))
                        for s in schema_types_list:       
                            if count == 0 or count%4 == 0:                            
                                print("{: >48}".format(s), end="")
                            elif count%4 < 3:                    
                                print("{: >48}".format(s), end="")        
                            else:
                                print("{: >48}".format(s))
                            count += 1
                        print("")
                        continue
                    elif suboption[2] == "versions":
                        print("Not Supported")
                        continue
                elif suboption[1] == "set":
                    if suboption[2] == CurrentSchemaLoad.lname:
                        print("Schema Bundle is Already Current")
                        continue
                    for slc in DRSchemaLoadList:
                        if slc.lname == suboption[2]:
                            CurrentSchemaLoad = slc
                            print("Setting Current Schema Bundle Information ")
                            print("ID: ", CurrentSchemaLoad.lname, "\tRedfish Schema: ", CurrentSchemaLoad.RedfishSDC.sdata.schemaName,"\tSwordfish Schema: ", CurrentSchemaLoad.SwordfishSDC.sdata.schemaName)
                            break                
                    continue
            elif len(suboption) == 4:
                if suboption[1] == "list":
                    if suboption[2] == "versions":                                    
                        schema_version_list = []
                        print("Listing Versions of Schema ",suboption[3])
                        for rp in CurrentSchemaLoad.SchemaBuild.RedfishSchemaDB.OptionsDB:
                            schemaPrefix = rp.SchemaData.schemaName.split(".")[0]
                            if suboption[3] == schemaPrefix:
                                if rp.key != schemaPrefix:
                                    continue
                                if len(rp.anyOf) > 0:   
                                    for r in rp.anyOf: 
                                        if r.Ref != None: 
                                            if r.Ref.Refdefinition != None:
                                                if r.Ref.Refdefinition.SchemaData.schemaName.startswith(schemaPrefix) == True:
                                                    schema_version_list.append(r.Ref.Refdefinition.SchemaData.schemaName.split(".")[1])
                        count = 0
                        for s in schema_version_list:       
                            if count == 0 or count%4 == 0:                            
                                print("{: >16}".format(s), end="")
                            elif count%4 < 3:                            
                                print("{: >16}".format(s), end="")
                            else:
                                print("{: >16}".format(s))
                            count += 1
                        print("")
        elif option.startswith("sc "):         
            suboption = option.split(" ")
            if len(suboption) == 1:
                if CurrentSchemaName == None:
                    print("No Schema Set ")
                    continue
                print("Current Schema Name = ", CurrentSchemaName, " Current Schema Version = ", CurrentSchemaVersion)
            elif len(suboption) == 2:
                if suboption[1] == "info":
                    if CurrentSchemaName == None:
                        print("No Schema Name Set ")
                        continue
                    if CurrentSchemaVersion == None:
                        print("No Schema Version Set ")
                        continue
                    SchemaInfo = CurrentSchemaName+"."+CurrentSchemaVersion+".json"
                    for rp in CurrentSchemaLoad.SchemaBuild.RedfishSchemaDB.OptionsDB:
                        if rp.SchemaData.schemaName == SchemaInfo:
                            print("Schema Header Information ")
                            print("id                             : ", rp.SchemaData.Header.Id)
                            print("owningEntity                   : ", rp.SchemaData.Header.owningEntity)
                            print("release                        : ", rp.SchemaData.Header.release)
                            print("title                          : ", rp.SchemaData.Header.title)
                            print("Schema Overview Information ")
                            print("{: >32} {: >12} {: >16} {: >16} {: <64}".format("Key","Type", "Properties", "Enums", "Description"))
                            for d in rp.SchemaData.definitionParList:                            
                                tp = "regular"
                                if d.deprecated != None:
                                    continue
                                if d.SchemaData.RootDefinitionParam == d:
                                    type = "root"
                                if len(d.description) > 64:
                                    print("{: >32} {: >12} {: >16} {: >16} {: <64}".format(d.key, type, len(d.properties), len(d.enumList), d.description[0:64]))
                                    length = len(d.description) - 64
                                    CurrentIndex = 64
                                    while length != 0: 
                                        if (CurrentIndex + 64) < length:
                                            print("{: >32} {: >12} {: >16} {: >16} {: <64}".format(" ", " ", " ", " ",d.description[CurrentIndex:CurrentIndex+64]))
                                            CurrentIndex += 64
                                        else:                                            
                                            print("{: >32} {: >12} {: >16} {: >16} {: <64}".format(" ", " ", " ", " ",d.description[CurrentIndex:CurrentIndex+(length - CurrentIndex)]))
                                            CurrentIndex += (length - CurrentIndex)
                                            break
                                else:
                                    print("{: >32} {: >12} {: >16} {: >16} {: <64}".format(d.key, type, len(d.properties), len(d.enumList), d.description))

                            print("\nSchema Properties Information ")
                            print("{: >32} {: >32} {: >8} {: <64}".format("Key","Prop Key", "Required", "Description"))
                            for d in rp.SchemaData.definitionParList:
                                if d.deprecated == None:
                                    for prop in d.properties:
                                        if prop.key.startswith("@odata") == True:
                                            continue;
                                        if prop.deprecated != None:
                                            continue;
                                        description = None
                                        if prop.description == None: 
                                            description = ""
                                        else:
                                            description = prop.description

                                        RequiredFlag = False
                                        if prop.key in rp.SchemaData.RootDefinitionParam.required:
                                            RequiredFlag = True
                                        if len(description) > 64:
                                            print("{: >32} {: >32} {: >8} {: <64}".format(rp.SchemaData.RootDefinitionParam.key, prop.key, RequiredFlag, description[0:64]))
                                            length = len(description) - 64
                                            CurrentIndex = 64
                                            while length != 0: 
                                                if (CurrentIndex + 64) < length:
                                                    print("{: >32} {: >32} {: >8} {: <64}".format("", "", "", description[CurrentIndex:CurrentIndex+64]))
                                                    CurrentIndex += 64
                                                else:
                                                    print("{: >32} {: >32} {: >8} {: <64}".format("", "", "", description[CurrentIndex:CurrentIndex+(length - CurrentIndex)]))                                                    
                                                    CurrentIndex += (length - CurrentIndex)
                                                    break
                                        else:
                                            print("{: >32} {: >32} {: >8} {: <64}".format(rp.SchemaData.RootDefinitionParam.key, prop.key, RequiredFlag, description))
                            print("\nSchema Enum Information ")
                            print("{: >32} {: >32} {: >32} {: >64}".format("Key","Enum Name", "Description", "Long Description"))

                            for d in rp.SchemaData.definitionParList:
                                if d.deprecated == None:
                                    if len(d.enumList) > 0:
                                        for enumdata in d.enumList:
                                            if enumdata.Deprecated != None:
                                                continue
                                            print("{: >32} {: >32} {: >32} {: >64}".format(d.key, enumdata.Name, enumdata.Description, enumdata.LongDescription))
                            break
            elif len(suboption) == 4:
                if suboption[1] == "set":
                    CurrentSchemaName = suboption[2]
                    CurrentSchemaVersion = suboption[3]
                    

           