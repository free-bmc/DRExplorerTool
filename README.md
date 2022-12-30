# DMTF Redfish Explorer Tool 
[Disclaimer:  This tool is not an official DMTF-Redfish tool approved by DMTF or SPMF, rather it is created to promote and increase adoption of DMTF-Redfish]
Tool to increase awareness of Redfish and help to define future Managed Hardware Platforms

## Introduction 
DMTF’s Redfish® is a standard designed to deliver simple and secure management for converged, hybrid IT and the Software Defined Data Center (SDDC). Both human readable and machine capable, Redfish leverages common Internet and web services standards to expose information directly to the modern tool chain

## Version History
### Version 1.0:
- DMTF Redfish and Swordfish Schema Bundles Discovery
- Download Redfish and Swordfish Schemas Bundles
- Analyze the Schema Bundles and Build a Schame Map (from ServiceRoot.json) with only valid Schemas Versions without Deprecated
- Schema Analysis for Headers, Properites, Definitions, Enum's 
- Allows loading multiple Schema bundles 

## Purpose of this tool
There are close to 3000+ schema files, which carry a lot of information that are gathered with collaborating across the industry, making it the single most valuable collection of information that can provide a wealth of data for requirements explorations and streamline the implementations. 

The schemas are created as standard guides, that would provide a means for both the customers and firmware vendors to HTTP requests and responses.  Most of the schemas provide a “required” property, that only covers a few and expects the customers and platform vendors to add the required properties as they negotiate and implement.   Unfortunately, most of the negotiations for these happen in excel spreadsheets or word documents, making it difficult to understand how they can be verified and ratified.

The schema tool provides the ability
    1. For Customers
        a. To provide their own derived schema bundle that would provide their own required properties in addition to what is specified in the standard schema
        b. To provide their required URIs that they are interested in
    2. For Firmware vendors
        a. To provide their derived schema bundles that would provide what properties and options they are providing in addition to the standard schema
        b. To publish their own set of URIs they support
    3. For Explorers        
        a. Understand how the URIs tree map works after synthesizing all the schemas 
        b. Explore the different enumerations of the different variables that are defined by Redfish
        c. Searching on the different schemas
        d. Selection of the versions for each schema
        e. Compare between 2 or more schema bundles to understand the compatibility and differences

The tool provides a pathway for these schemas to not only be used for validation but also used for the customers to build their derived schemas that would present their expectations to the vendors, and also allow the vendors to provide their own firmware implementations features and capabilities in a standardized way.

Please note
    1. The tool only includes those schemas that are referenced by schemas traceable to ServiceRoot.json
    2. The tool automatically removes those properties that are deprecated from the specific schema versions

## Next version has
    1. Saving your changes to a derived schema bundle
    2. Comparing the derived schema bundles
    3. Adding a project infrastructure to add more information about the editor, company name, credentials etc.

### Tool Setup 

Tool goes it own setup when first started,  please use DRExplorerTool.py to start the tool, note: the tool creates a DRExplorerHome in your HOME directory

### Tool Usage 

```
Welcome to DMTF Redfish Explorer Utility
The Tool that allows to Explore DMTF Redfish and Swordfish Schema bundles
The tool parses through the Schema bundle from ServiceRoot.json and connects them together

The tool features :
 1. Check the DMTF Redfish and Swordfish and get the list of available Schema Bundles to download
 2. Download the DMTF Redfish and Swordfish Schema bundles
 3. Load and Explore the Schemas and get more information
 4. CLI that supports exploration


Setup In Progress...
First Time Setup ...
Please be patient will take few minutes to set up...
Scanning for DMTF Redfish Schema Bundles ... Found  24
Scanning for DMTF Swordfish Schema Bundles ... Found  2
Setup Complete, Ready to Explore ...
CLI started ...
RSE CLI >> help
Commands and Options:
        version       <options>                Version Info
        rflist                                 List DMTF Redfish Schema Bundle
        sflist                                 List DMTF Swordfish Schema Bundle
        download                               Download Schema Bundle
        load [ ,schema,<ID>]                   Load Redfish Schema Bundle Options
                                               No Arg - List Loaded Schema Bundle
                                               schema - Loaded a Schema Bundle
                                               <ID> -   Loaded Schema Bundle with ID

        sb <options>                           Schema Bundle Options
                                               No Arg                  - Display Current Schema Bundle
                                               set <ID>                - Set the Schema Bundle
                                               info                    - Schema Bundle info
                                               urimap                  - URI Map
                                               list schemas            - List Schemas
                                               list versions <schema>  - List Schema Versions

        sc <options>                           Schema Options
                                               No Arg                  - Display Current Schema, Version
                                               set <Schema> <Version   - Set the Schema and Version
                                               info                    - Schema info
RSE CLI >> rflist
Available DMTF Redfish Schema List
rf1      DSP8010_2022.2          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2022.2.zip
rf2      DSP8010_2022.1          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2022.1.zip
rf3      DSP8010_2021.4_0        https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2021.4_0.zip
rf4      DSP8010_2021.3          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2021.3.zip
rf5      DSP8010_2021.2          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2021.2.zip
rf6      DSP8010_2021.1          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2021.1.zip
rf7      DSP8010_2020.4          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2020.4.zip
rf8      DSP8010_2020.3          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2020.3.zip
rf9      DSP8010_2020.2          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2020.2.zip
rf10     DSP8010_2020.1          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2020.1.zip
rf11     DSP8010_2019.4          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2019.4.zip
rf12     DSP8010_2019.3          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2019.3.zip
rf13     DSP8010_2019.2          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2019.2.zip
rf14     DSP8010_2019.1_1        https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2019.1_1.zip
rf15     DSP8010_2018.3          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2018.3.zip
rf16     DSP8010_2018.2          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2018.2.zip
rf17     DSP8010_2018.1          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2018.1.zip
rf18     DSP8010_2017.3          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2017.3.zip
rf19     DSP8010_2017.2          http://redfish.dmtf.org/schemas/DSP8010_2017.2.zip
rf20     DSP8010_2017.1          http://redfish.dmtf.org/schemas/DSP8010_2017.1.zip
rf21     DSP8010_2016.3          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2016.3.zip
rf22     DSP8010_2016.2          http://redfish.dmtf.org/schemas/archive/2016.2/DSP8010_2016.2.zip
rf23     DSP8010_2016.1          https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_2016.1.zip
rf24     DSP8010_1.0.0   https://www.dmtf.org/sites/default/files/standards/documents/DSP8010_1.0.0.zip
RSE CLI >> sflist
Available DMTF Swordfish Schema List
sf1      Swordfish_v1.2.4_Schema         https://www.snia.org/sites/default/files/technical-work/swordfish/draft/v1.2.4/zip/Swordfish_v1.2.4_Schema.zip
sf2      Swordfish_v1.2.4a_Schema        https://www.snia.org/sites/default/files/technical-work/swordfish/release/v1.2.4a/zip/Swordfish_v1.2.4a_Schema.zip
RSE CLI >> download
ID      Schema Name             Schema Type
rf1      DSP8010_2022.2          Redfish
Do you want to continue to Download Y/N Y
Choose one or more shortcuts to download, use , for multiple downloads sf1
Retriving  Swordfish_v1.2.4_Schema From  https://www.snia.org/sites/default/files/technical-work/swordfish/draft/v1.2.4/zip/Swordfish_v1.2.4_Schema.zip
RSE CLI >>

RSE CLI >> load
ID      Redfish Schema           Swordfish Schema
RSE CLI >> load schema
Redfish Schemas Download List:
        ID      Schema Name
         rf1     DSP8010_2022.2
Select Schema (use ID): rf1
Swordfish Schemas Download List:
        ID      Schema Name
         sf1     Swordfish_v1.2.4_Schema
Select Schema (use ID): sf1
Select a unique ID for this Load Combination: First
Loading Schema Bundle : [####################################################################################################] 1/1
Loading is Completed...
Schema Loaded and Ready for exploration
RSE CLI >> load
ID      Redfish Schema           Swordfish Schema
First    DSP8010_2022.2          Swordfish_v1.2.4_Schema
RSE CLI >>

```

If you have any questions or suggestions, please email to haveuthoughtaboutit@gmail.com