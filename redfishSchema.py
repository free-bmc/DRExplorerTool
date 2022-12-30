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

import os
import json
import sys

from urllib.request import urlopen

class refDataClass:
    def __init__(self):
        self.Ref = None
        self.schemaName = None
        self.Refdefinition = None

class redfishEnumElementClass:
    def __init__(self, name):
        self.Name = name
        self.Description = None
        self.LongDescription = None
        self.VersionAdded = None
        self.Deprecated = None
        self.VersionDeprecated = None

class redfishParametersClass:
    def __init__(self, schema, k, paramType, parent):
        self.ParamType = paramType
        self.Parent = parent
        self.SchemaData = schema
        self.key = k
        self.anyOf = []
        self.properties = []
        self.Ref = None
        self.readonly = False
        self.type = None
        self.description = None
        self.additionalProperties = None
        self.requiredOnCreate = []
        self.requiredParameter = False
        self.longDescription = None
        self.copyright = None
        self.deprecated = None
        self.versionDeprecated = None
        self.versionAdded = None
        self.enumDescriptions = None
        self.enumLongDescriptions = None
        self.enumDeprecated = None
        self.enumVersionDeprecated = None
        self.enumVersionAdded = None
        self.units = None
        self.owningEntity = None
        self.excerpt = None
        self.excerptCopy = None
        self.excerptCopyOnly = False
        self.insertable = False
        self.updatable = False
        self.deletable = False
        self.uris = []
        self.autoExpand = False
        self.release = None
        self.filter = None
        self.language = None
        self.translation = None
        self.enumTranslations = None
        self.actionResponse = None
        self.license = None
        self.releaseStatus = ["Standard", "Informational", "WorkInProgress", "InDevelopment"]
        self.required = []
        self.patternProperties = None
        self.items = None
        self.itemsRef = None
        self.pattern = None
        self.format = None
        self.enum_data = None
        self.minimum = 0
        self.maximum = 0
        self.enumList = []
    
    def redfishDefinitionFillParameters(self, jObject):
        
        if jObject.get("anyOf") != None:
            if type(jObject.get("anyOf")) is list:
                AnyOfObject = jObject.get("anyOf")
                for jelement in AnyOfObject:
                    rParam = redfishParametersClass(self.SchemaData, None, "anyOf", self)
                    rParam.redfishDefinitionFillParameters(jelement)
                    self.anyOf.append(rParam)                

                self.SchemaData.SchemaDB.OptionsDB.append(self)            

        if jObject.get("properties") != None:
            if type(jObject.get("properties")) is dict:
                propertiesObject = jObject.get("properties")
                keylist = list(propertiesObject.keys())
                for i in range(0, len(propertiesObject)):
                    rParam = redfishParametersClass(self.SchemaData, keylist[i], "Property", self)
                    rParam.redfishDefinitionFillParameters(propertiesObject.get(keylist[i]))
                    self.properties.append(rParam)
                    self.SchemaData.SchemaDB.PropertiesListDB.append(rParam)

        if jObject.get("$ref") != None:
            ref = jObject.get("$ref").strip()
            self.Ref = refDataClass()
            self.ProcessRef(ref, self.Ref)
        
        if jObject.get("type") != None:
            self.type =  jObject.get("type")
        
        if jObject.get("description") != None:
            self.description =  jObject.get("description")
        
        if jObject.get("readonly") != None:
            self.readonly =  jObject.get("readonly")
        
        if jObject.get("additionalProperties") != None: 
            self.additionalProperties =  jObject.get("additionalProperties")

        if jObject.get("requiredParameter") != None: 
            self.requiredParameter =  jObject.get("requiredParameter")

        if jObject.get("longDescription") != None: 
            self.longDescription =  jObject.get("longDescription")

        if jObject.get("copyright") != None: 
            self.copyright =  jObject.get("copyright")

        if jObject.get("deprecated") != None: 
            self.deprecated =  jObject.get("deprecated")

        if jObject.get("versionDeprecated") != None: 
            self.versionDeprecated =  jObject.get("versionDeprecated")

        if jObject.get("versionAdded") != None: 
            self.versionAdded =  jObject.get("versionAdded")

        if jObject.get("enumDescriptions") != None: 
            self.enumDescriptions =  jObject.get("enumDescriptions")

        if jObject.get("enumLongDescriptions") != None: 
            self.enumLongDescriptions =  jObject.get("enumLongDescriptions")

        if jObject.get("enumDeprecated") != None: 
            self.enumDeprecated =  jObject.get("enumDeprecated")

        if jObject.get("enumVersionDeprecated") != None: 
            self.enumVersionDeprecated =  jObject.get("enumVersionDeprecated")

        if jObject.get("enumVersionAdded") != None: 
            self.enumVersionAdded =  jObject.get("enumVersionAdded")

        if jObject.get("units") != None: 
            self.units =  jObject.get("units")

        if jObject.get("owningEntity") != None: 
            self.owningEntity =  jObject.get("owningEntity")

        if jObject.get("excerpt") != None: 
            self.excerpt =  jObject.get("excerpt")

        if jObject.get("excerptCopy") != None: 
            self.excerptCopy =  jObject.get("excerptCopy")

        if jObject.get("excerptCopyOnly") != None: 
            self.excerptCopyOnly =  jObject.get("excerptCopyOnly")

        if jObject.get("insertable") != None: 
            self.insertable =  jObject.get("insertable")

        if jObject.get("updatable") != None: 
            self.updatable =  jObject.get("updatable")

        if jObject.get("deletable") != None: 
            self.deletable =  jObject.get("deletable")

        if jObject.get("autoExpand") != None: 
            self.autoExpand =  jObject.get("autoExpand")

        if jObject.get("release") != None: 
            self.release =  jObject.get("release")

        if jObject.get("filter") != None: 
            self.self.filter =  jObject.get("filter")

        if jObject.get("language") != None: 
            self.language =  jObject.get("language")

        if jObject.get("translation") != None: 
            self.translation =  jObject.get("translation")

        if jObject.get("enumTranslations") != None: 
            self.enumTranslations =  jObject.get("enumTranslations")

        if jObject.get("actionResponse") != None: 
            self.actionResponse =  jObject.get("actionResponse")

        if jObject.get("license") != None: 
            license =  jObject.get("license")
        
        if jObject.get("uris") != None:
            for jElement in jObject.get("uris"):
                self.uris.append(jElement)
                uriinfo = UriInfoClass(jElement, self)
                self.SchemaData.SchemaDB.UriList.append(uriinfo)

        if jObject.get("required") != None:
            for jElement in jObject.get("required"):
                self.required.append(jElement)
        
        if jObject.get("items") != None:
            self.items =  jObject.get("items")
            if type(self.items) is dict:
                keylist = list(jObject.get("items").keys())
                for key in keylist:
                    if key == "$ref":
                        ref = self.items.get(key).strip()
                        self.itemsRef = refDataClass()
                        self.ProcessRef(ref, self.itemsRef)                    

                if type(self.items.get(key)) is list: 
                    AnyOfObject = self.items.get(key)
                    for jelement in AnyOfObject:
                        if type(jelement) is dict:
                            if jelement.get("$ref") != None:
                                ref = jelement.get("$ref").strip()
                                self.itemsRef = refDataClass()
                                self.ProcessRef(ref, self.itemsRef)                                                
        
        if jObject.get("pattern") != None:
            self.pattern =  jObject.get("pattern")
        if jObject.get("format") != None:
            self.format =  jObject.get("format")
        if jObject.get("minimum") != None:
            self.minimum =  jObject.get("minimum")
        if jObject.get("maximum") != None:
            self.maximum =  jObject.get("maximum")

        if jObject.get("enum") != None:
            if type(jObject.get("enum")) is list:
                self.enum_data =  jObject.get("enum")

            for jelement in self.enum_data:
                ree = redfishEnumElementClass(jelement)
                ree.Description = self.GetValue(jelement, self.enumDescriptions)
                ree.LongDescription = self.GetValue(jelement, self.enumLongDescriptions)
                ree.VersionAdded = self.GetValue(jelement, self.enumVersionAdded)
                ree.Deprecated = self.GetValue(jelement, self.enumDeprecated)
                ree.VersionDeprecated = self.GetValue(jelement, self.enumVersionDeprecated)
                self.enumList.append(ree)

            self.SchemaData.SchemaDB.EnumListDB.append(self)
        
        t_pclass = redfishParametersClass(None, None, None, None)
        ClassFields = vars(t_pclass)
        ClassFieldKeys = ClassFields.keys()
        keylist = jObject.keys()

        for key in keylist:        
            key_found = False
            for field in ClassFieldKeys:
                if key == field:
                    key_found = True
                    break            

            if key_found == False:
                if key in self.SchemaData.SchemaDB.UnprocessedList == False:
                    self.SchemaData.SchemaDB.UnprocessedList.append(key)                

        self.SchemaData.SchemaDB.DefinitionsDB.append(self)
        
    def GetValue(self, key,  jObject):
        if jObject == None:
            return None

        if jObject.get(key) == None:
            return None
        
        return jObject.get(key)

    def ProcessRef(self, ref, refData):
        if "http" in ref:
            match_found = False
            schemaFileURL = ref.split("#")[0]
            schemaName = schemaFileURL.split("/")[len(schemaFileURL.split("/")) - 1]
            for rData in self.SchemaData.SchemaDB.ImportRefList:
                if rData.schemaName == schemaName:
                    match_found = True
                    break

            if match_found == False:
                refData.Ref = ref                
                refData.schemaName = schemaName
                self.SchemaData.DependentList.append(refData)
                self.SchemaData.SchemaDB.ImportRefList.append(refData)
        else:
            match_found = False
            for rData in self.SchemaData.LocalRefList:
                if rData.Ref == ref:
                    match_found = True

            if match_found == False:
                refData.Ref = ref
                self.SchemaData.LocalRefList.append(refData)

class redfishSchemaHeaderClass:
    def __init__(self, filename, jObject):            
        self.Id = None
        self.Schema = None
        self.Ref = None
        self.type = None
        self.copyright = None
        self.owningEntity = None
        self.release = None
        self.title = None
    
        if jObject.get("$id") != None:
            self.Id = jObject.get("$id")

        if jObject.get("$schema") != None:
            self.Schema = jObject.get("$schema")

        if jObject.get("$ref") != None:
            self.Ref = jObject.get("$ref")

        if jObject.get("type") != None:
            self.type = jObject.get("type")

        if jObject.get("copyright") != None:
            self.copyright = jObject.get("copyright")

        if jObject.get("owningEntity") != None:
            self.owningEntity = jObject.get("owningEntity")

        if jObject.get("release") != None:
            self.release = jObject.get("release")

        if jObject.get("title") != None:
            self.title = jObject.get("title")

class redfishSchemaDataClass:
    def __init__(self, schemaDB):
        self.SchemaDB = schemaDB
        self.FileString = None
        self.FileJsonObject = None
        self.RootObject = None
        self.RootdefinitionsObject = None
        self.RootDefinitionString = None
        
        self.RootDefinitionParam = None
        self.definitionsObject = None
        
        self.schemaFile = None
        self.schemaUrl = None
        self.schemaName = None
        
        self.DependentList = []
        self.Header = None
        self.definitionParList = []
        self.LocalRefList = []

    def JsonObjectFromFile(self, file):
        self.schemaFile = file
        directory, fname = os.path.split(file.name)
        self.schemaName = fname
        jObject = json.load(file)

        self.Header = redfishSchemaHeaderClass(self.schemaFile.name, jObject)
        if self.Header.Ref != None:
            mainDef = jObject.get("$ref").split("/")
            
            tmpObject = jObject
            for i in range(1, len(mainDef)):
                tmpObject = tmpObject.get(mainDef[i])

            self.RootObject = jObject
            self.RootDefinitionString = mainDef[len(mainDef)-1]
            self.RootdefinitionsObject = tmpObject   
            self.definitionsObject= jObject.get("definitions")
        else:
            if jObject.get("definitions") != None:
                self.definitionsObject = jObject.get("definitions")
        file.close()

    def JsonObjectFromString(self, jString, Url):
        self.schemaUrl = Url
        self.schemaName = Url.split("/")[len(Url.split("/")) - 1]
        jObject = json.loads(jString)
        self.FileJsonObject = jObject
        self.FileString = jString
        self.Header = redfishSchemaHeaderClass(None, jObject)
        if self.Header.Ref != None:
            mainDef = jObject.get("$ref").split("/")
            tmpObject = jObject
            for i in range(1, len(mainDef)):
                tmpObject = tmpObject.get(mainDef[i])

            self.RootObject = jObject
            self.RootDefinitionString = mainDef[len(mainDef)-1]
            self.RootdefinitionsObject = tmpObject
            self.definitionsObject= jObject.get("definitions")
        else:
            if jObject.get("definitions") != None:
                self.definitionsObject = jObject.get("definitions")
    
    def SaveJsonFile(self,directory):
        WriterFile = os.path.abspath(directory)+"/"+self.schemaName
        with open(WriterFile, "w") as outfile:
            outfile.write(self.FileString)

    def SchemaData(self):
        if self.RootdefinitionsObject != None:
            rfParam = redfishParametersClass(self, self.RootDefinitionString, "Definition", None)
            rfParam.redfishDefinitionFillParameters(self.RootdefinitionsObject)
            self.RootDefinitionParam = rfParam
            self.definitionParList.append(rfParam)
        elif self.definitionsObject != None:
            keylist = self.definitionsObject.keys()
            for key in keylist:
                rfParam = redfishParametersClass(self, key, "Definition", None)
                rfParam.redfishDefinitionFillParameters(self.definitionsObject.get(key))
                self.definitionParList.append(rfParam)
        
        while len(self.LocalRefList) != 0:
            self.ResolveLocalReferences()
            
    def ResolveLocalReferences(self):
        # Resolve internal references 
        RefList = self.LocalRefList.copy()
        self.LocalRefList.clear()
        for ref in RefList:
            definitionString = ref.Ref.replace("#/definitions/", "").replace("\"", "")
            found = False
            for rdc in self.definitionParList:
                if definitionString == rdc.key:
                    ref.Refdefinition = rdc
                    found = True

            if found == False:
                keylist = self.definitionsObject.keys()
                for key in keylist:
                    if key == definitionString:
                        rfParam = redfishParametersClass(self, key, "Definition", None)
                        rfParam.redfishDefinitionFillParameters(self.definitionsObject.get(key))
                        ref.Refdefinition = rfParam
                        self.SchemaDB.DefinitionsDB.append(rfParam)
                        self.definitionParList.append(rfParam)

                        if len(rfParam.enumList) > 0:
                            self.SchemaDB.EnumListDB.append(rfParam)

    def UpdateDefinition(self, refd):
        ref = None
        if "definitions" in refd:
            ref = refd.replace("#/definitions/","")
        else:
            ref = refd

        keylist = self.definitionsObject.keys()           
        for key in keylist:
            if key == ref:
                rfParam = redfishParametersClass(self, key, "Definition", None)
                rfParam.redfishDefinitionFillParameters(self.definitionsObject.get(key))
                self.definitionParList.append(rfParam)
                self.SchemaDB.DefinitionsDB.append(rfParam)
                if len(rfParam.enumList) > 0:
                    self.SchemaDB.EnumListDB.append(rfParam)
                return rfParam
        
        return None

class DSP8010VersionInfoClass:
    def __init__(self):
        self.version = None
        self.title = None
        self.URLBundle = None
        self.pubdate = None
        self.comments = None

class RedfishSchemaDBClass:
    def __init__(self):
        self.RedfishSchemaFullList = []
        self.RedfishSchemaUrlList = []
        self.RedfishSchemaList =[]
        self.RedfishServiceRoot = []
        self.ServiceRootSchemaData = None        
        self.EnumListDB = []
        self.PropertiesListDB = []
        self.DefinitionsDB = []
        self.OptionsDB = []        
        self.ExternalRefElementList = []
        self.FullUriList = []
        self.URLUriList = []
        self.UriList = []
        self.ImportRefList = []        
        self.redfishDefinitionsStats = 0
        self.redfishRefStats = 0
        self.redfishExternalRefStats = 0
        self.local_flag = False
        self.unfounded_check = False
        self.UriFullLayout = None
        self.UriURLLayout = None
        self.UriLayout = None            
        self.UnprocessedList = []
        self.progress_counter = 0
        self.DSP8010VersionInfo = []
        self.LocalRedfishDiskDirectory = None
        self.LocalSwordfishDiskDirectory = None
    

    def PerformLocalDiskSchemaParsing(self, directory):
    
        self.RedfishSchemaList = self.RedfishSchemaFullList
        self.UriList = self.FullUriList
        self.LocalDiskDirectory = directory
        ServiceRootFile = os.path.abspath(directory)+"/ServiceRoot.json"
        if os.path.exists(ServiceRootFile):
            return False
        
        # Time Monitoring Start
        rsc = redfishSchemaDataClass(self)
        rsc.JsonObjectFromFile(ServiceRootFile)
        rsc.SchemaData()
        self.RedfishSchemaList.append(rsc)
        
        while len(self.ImportRefList) != 0:
            self.ResolveReferences()
        
        # Time Monitoring Stop
        return True
        
    def StartLocalDiskSchemaParsing(self, redfishdirectory, swordfishdirectory):

        self.RedfishSchemaList = self.RedfishSchemaFullList
        self.UriList = self.FullUriList
        self.LocalRedfishDiskDirectory = redfishdirectory
        self.LocalSwordfishDiskDirectory = swordfishdirectory
        ServiceRootFile = redfishdirectory +"/ServiceRoot.json"
        if os.path.exists(ServiceRootFile) == False:
            return False        
        # Time Monitoring Start
        rsc = redfishSchemaDataClass(self)
        #print(ServiceRootFile)
        rsc.JsonObjectFromFile(open(ServiceRootFile))
        rsc.SchemaData()
        self.RedfishSchemaList.append(rsc)
        
        return True
    
    def SaveSchemaFiles(self, directory):
        for rsd in self.RedfishSchemaList:
            rsd.SaveJsonFile(directory)            
    
    def PerformUrlRedfishSchemaParsing(self):
        #Instant start, finish
        
        self.RedfishSchemaList = self.RedfishSchemaUrlList
        self.UriList = self.FullUriList
        #start = Instant.now()
        
        
        f = urlopen("http://redfish.dmtf.org/schemas/v1/ServiceRoot.json")
        jsonData = f.read()

        if jsonData != None:
            rsc = redfishSchemaDataClass(self)
            rsc.JsonObjectFromString(jsonData,"http://redfish.dmtf.org/schemas/v1/ServiceRoot.json")
            rsc.SchemaData()
            self.ServiceRootSchemaData = rsc
            self.RedfishSchemaList.append(rsc)

        self.progress_counter = len(self.RedfishSchemaList)
        
        while len(self.ImportRefList) != 0:
            self.ResolveReferences()
        
        #finish = Instant.now()
                
        UnFoundSchemaList = []

    def StartUrlRedfishSchemaParsing(self):
        #Instant start, finish
        
        self.RedfishSchemaList = self.RedfishSchemaUrlList
        self.UriList = self.FullUriList
  
        #start = Instant.now()
        f = urlopen("http://redfish.dmtf.org/schemas/v1/ServiceRoot.json")
        jsonData = f.read()
        if jsonData != None:
            rsc = redfishSchemaDataClass(self)
            rsc.JsonObjectFromString(jsonData,"http://redfish.dmtf.org/schemas/v1/ServiceRoot.json")
            rsc.SchemaData()
            self.ServiceRootSchemaData = rsc
            self.RedfishSchemaList.append(rsc)

        self.progress_counter = len(self.RedfishSchemaList)
    
    def ResolveReferences(self):
        processList = self.ImportRefList.copy()
        self.ImportRefList.clear()        

        for ref in processList:
            local_found = False
            definitionString = "#" + ref.Ref.split("#")[1].replace("\"", "")
            index = 0
            for index in range(0, len(self.RedfishSchemaList)):
                schema_found = False
                rsd = self.RedfishSchemaList[index]

                if ref.schemaName == rsd.schemaName:
                    schema_found = True

                if schema_found == True:
                    key = definitionString.replace("#/definitions/","")
                    for rdc in rsd.definitionParList:
                        if key == rdc.key:
                            ref.Refdefinition = rdc
                            local_found = True

                    if local_found == True:
                        break
                    else:
                        ref.Refdefinition = rsd.UpdateDefinition(definitionString)
                        if ref.Refdefinition != None:
                            local_found = True
                            break
            
            if local_found == False:
                self.ExternalRefElementList.append(ref)

        self.redfishRefStats += len(processList)
        
        for ref in self.ExternalRefElementList:
            found =  False
            jsonData = None
            
            if ref.Ref == None:
                continue
            
            schemaFileURL = ref.Ref.split("#")[0].replace("\"", "")
            schemaFileString = schemaFileURL.split("/")[len(schemaFileURL.split("/")) - 1]            
            definitionString =ref.Ref.split("#")[1].replace("\"", "").replace("/definitions/", "")
            
            # Adding references that are not part of redfish v1 schemas
            rsc = None
            
            if self.LocalRedfishDiskDirectory != None:
                if "swordfish" in schemaFileURL:
                    schemaFile = self.LocalSwordfishDiskDirectory+"/"+schemaFileString
                else:
                    schemaFile = self.LocalRedfishDiskDirectory+"/"+schemaFileString
                if os.path.exists(schemaFile) == True:
                    rsc =redfishSchemaDataClass(self)
                    #print(schemaFile)
                    rsc.JsonObjectFromFile(open(schemaFile, "r"))
                else:
                    print("Not Found",schemaFile)
            if rsc != None:
                if "ServiceRoot.v" in rsc.schemaName:
                    self.RedfishServiceRoot = rsc

            if rsc != None:
                rsc.SchemaData()
                self.RedfishSchemaList.append(rsc)
                
                if len(rsc.definitionParList) > 0:
                    for rdc in rsc.definitionParList:
                        if definitionString == rdc.key:
                            ref.Refdefinition = rdc
                            found = True
                            break

                    if found == False:
                        ref.Refdefinition = rsc.UpdateDefinition(definitionString)

        self.redfishExternalRefStats += len(self.ExternalRefElementList)
        self.ExternalRefElementList.clear()

    def ProcessUriList(self):
        for uri in self.UriList:
            if self.UriURLLayout == None:
                self.UriURLLayout = UriLayoutClass(uri, "redfish", 0)
                self.UriLayout = self.UriURLLayout

            self.UriLayout.AddUri(uri,uri.uri.split("/"), 1)            

    def GetFileFromLocal(filename):
        directory = os.scandir("/home/hari/DSP8010_2022.2/json-schema")
        for entry in directory:
            if entry.name == filename:
                return entry

        return None                    

class UriInfoClass:
    def __init__(self, u, r):
        self.uri = u
        self.ParamRef = r

class UriLayoutClass:
    def __init__(self, uriinfo, layerinfo, l ):
        self.UriInfo = uriinfo
        self.level = l
        self.layer = layerinfo
        self.layerList = []
    
    def AddUri(self, uriinfo, layerinfo, lvl ):
        found = False
        if (lvl+1) == len(layerinfo):
                return

        for  u in self.layerList:
            if layerinfo[lvl+1] in u.layer:
                u.AddUri(uriinfo, layerinfo, lvl+1)
                found = True

        if found == False:
            u = UriLayoutClass(uriinfo, layerinfo[lvl+1], lvl+1)
            self.layerList.append(u)
            u.AddUri(uriinfo, layerinfo, lvl+1)
        
    def URLString(self):
        s = self.UriInfo.uri.split("/")
        urlstring = None
        if self.level == 0:
            return ""
        urlstring = ""
        for i in range(0, self.level+1):
            urlstring += ("/"+s[i])

        return urlstring
    
    def PrintUri(self):
        sp = ""
        for i in range(0, self.level):
            sp += " "
        print("\r", sp, self.layer,"\t",self.URLString())
        for u in self.layerList:
            u.PrintUri()

class RedfishSchemaBuildClass:
    def __init__(self, source, localRedfishDirectory, localSwordfishDirectory):
        self.RedfishSchemaDB = None
        self.LoadSchemaFromDMTF = False
        self.LoadSchemaFromDisk = False
        self.SaveSchemaToDisk = False
    
        self.Source = source 
        self.SchemaBundleVersion = None
        self.LocalRedfishDirectory = localRedfishDirectory
        self.LocalSwordfishDirectory = localSwordfishDirectory
        self.RedfishSchemaDB = RedfishSchemaDBClass()

        
    def RedfishSchemaBuild(self):        
        #print("Wait Loading in Progress...")
        if self.LoadSchemaFromDMTF == True:
            self.RedfishSchemaDB.StartUrlRedfishSchemaParsing()
        else:
            self.RedfishSchemaDB.StartLocalDiskSchemaParsing(self.LocalRedfishDirectory, self.LocalSwordfishDirectory)

        for i in progressbar(range(len(self.RedfishSchemaDB.RedfishSchemaList)), "Loading Schema Bundle : ", 100):
            while len(self.RedfishSchemaDB.ImportRefList) != 0:
                self.RedfishSchemaDB.ResolveReferences()
            #print(len(self.RedfishSchemaDB.RedfishSchemaList))

        self.RedfishSchemaDB.ProcessUriList()

        print("Loading is Completed...")

class SchemaInfoClass:
    def __init__(self, name, url, shortcut):
        self.schemaName = name
        self.URL = url
        self.ShortCut = shortcut

class SchemaLoadClass:
    def __init__(self, lname, rfsdc, sfsdc, schemabuild):
        self.lname = lname
        self.SchemaBuild = schemabuild
        self.RedfishSDC = rfsdc
        self.SwordfishSDC = sfsdc

class SchemaDownloadClass:
    def __init__(self, dir, sdata, fentry):
        self.dir = dir
        self.sdata = sdata
        self.fentry = fentry

def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.6+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print(f"{prefix}[{'#'*x}{('.'*(size-x))}] {j}/{count}", end='\r', file=out, flush=True)
        #print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count}", end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("", flush=True, file=out)