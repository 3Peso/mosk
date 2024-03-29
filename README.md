# mosk

mosk is a short form for "macOS Kraken". Originally created as framework to collect artefacts from macOS images and machines running macOS. The framework is designed to be easyly extensible with additional collector classes.

mosk should not only run collectors to collect artefacts, it should also provide some layer of documentation of what has been collected and how this happend, to be able to later explain the "what", "when" and the "how" to others.

## Instructions

To run mosk you have to provide instructions provided, for example, as XML files.

### Example Instruction XML
```xml
<Task>
    <TaskHeader>
        <examiner title="Examiner">
            !@examiner@!
        </examiner>
        <originaltask title="Assignment">
            !@clienttask@!
        </originaltask>
        <taskissuer title="Client">
            !@client@!
        </taskissuer>
        <artefactdescription title="Description of Artefact">
            !@artefactdescription@!
        </artefactdescription>
        <taskdescription title="Task Description">
            Colellect everything you can.
        </taskdescription>
    </TaskHeader>
    <Instructions>
        <Root module="source.root">
            <LocalHost module="source.localhost">
                <MachineName module="artefact.localhost.machineinformation" placeholdername="machinename" />
            </LocalHost>
            <LocalHost path="!@machinename@!" module="source.localhost">
                <OSName module="artefact.localhost.osinformation" />
                <OSVersion module="artefact.localhost.osinformation" />
                <OSTimezone module="artefact.localhost.osinformation" />
                <LocalTime module="artefact.localhost.system"
                description="Some describing text for the collector which will be logged in protocol metadata."/>
            </LocalHost>
            <Network module="source.network">
                <TimeFromNTPServer module="artefact.network.system" />
            </Network>
        </Root>
    </Instructions>
</Task>
```

As instructions format currently only XML is supported.

### XML Instructions Schema

The instrucitons are validated against this XML schema:
```xml
<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="Task">
    <xs:complexType>
      <xs:sequence>
          <xs:element type="TaskHeader" name="TaskHeader" minOccurs="0" maxOccurs="unbounded" ></xs:element>
          <xs:element type="Instructions" name="Instructions"></xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <xs:complexType name="TaskHeader">
    <xs:sequence>
      <xs:any minOccurs="0" maxOccurs="unbounded" processContents="lax" />
    </xs:sequence>
  </xs:complexType>

  <xs:complexType name="Instructions">
    <xs:choice>
      <xs:element type="Root" name="Root" />
    </xs:choice>
  </xs:complexType>

  <xs:complexType name="Root">
    <xs:sequence>
      <xs:any processContents="skip" minOccurs="0" maxOccurs="unbounded" />
    </xs:sequence>
    <xs:attribute name="module" type="xs:string" />
  </xs:complexType>
</xs:schema>
```

### XML Instruction Definition

If you want to add a collector to the instructions you have to use the class name of the collector as element name, and provide the module in the attribute 'module' like for example:

```xml
...
    <OSTimezone module="artefact.localhost.osinformation" />
...
```

#### Attributes

There are several attributes, which are [reserved](#Reserved%20Attributes) for use by mosk itself. But appart from that you can define
as much attributes for a collector as you want. This, of course mean, that the content of these attributes 
will not do much, except, it will be logged along side with other information inside the collection 
protocol. So, you can use this to document things for later. For example:

```XML
<PLUtil module="artefact.localhost.tools"
        source_path="~/Library/Application Support/com.apple.backgroundtaskmanagementagent/backgrounditems.btm"
        first_supported_mac_os_version="10.13 (High Sierra)"
        tool_path="./external_tools/plutil"
        description="Plists listing applications that automatically start when the user is logged in. Managed by the user through settings." />
```

The above collector has two attributes, `first_supported_mac_os_version` and `description`, which will server
only for documentation purposes. There is no other functionalliy behind them. BUT, you are absolutely free
to define any attributes you want here.

The result in the text protocol would look something like the following:

```
*****************************
Root:0->LocalHost:1->PLUtil:2
*****************************
Title: PLUtil
Description: Lists the contents of a provided plist file.
Collection Method: Uses the system command 'plutil' with -p
 
-- Collection Data     ----------

{
    SNIP
}


-- Collection Metadata ----------
Collection Time Stamp: 2021-12-04 08:36:36.377666
Source MD5: 1cdeafe9c2c549c796ac8bec07fa0789
Source path: SNIP 
Collector: artefact.localhost.tools.PLUtil
tool_path: './external_tools/plutil'
source_path: '~/Library/Application Support/com.apple.backgroundtaskmanagementagent/backgrounditems.btm'
first_supported_mac_os_version: '10.13 (High Sierra)'
description: 'Plists listing applications that automatically start when the user is logged in. 
 Managed by the user through settings.'
---------------------------------
```

##### Reserved Attributes

*Has to be initialized*

### Placeholders

You can define placeholders inside the instructions enclosed by '!@' '@!', 
for example '!@test@!. mosk will try to fill in the "blanks" in two runs. First 
run is before the actual collectors are been instanciated. You can provide the 
values for this in the file 'global_placeholders.json'. Second run actually 
happens during collection. If one collector collects the value for the 
placeholder before another collector consumes it.

Currently only XML is supported as instructions format. So currently the only 
way to provide values for placeholders collected by collectors is by providing 
the attribute "placeholdername" for the collector which should collect the value 
for later use.

Example:

```xml
            <LocalHost module="source.localhost">-->
                <MachineName module="artefact.localhost.machineinformation" placeholdername="machinename" />
            </LocalHost>
            <LocalHost path="!@machinename@!" module="source.localhost">
              ...
            </LocalHost>
```
The above example also implies that you can reuse placeholders throught the 
instructions as often as you want, as long as they already have been intiailzed 
before usage.

### 'global_placeholders.json'

You can provide placeholders in a global placeholder file, by default "global_placeholders.json":

```json
{
  "examiner": "sho",
  "clienttask": "Collect data artefacts regarding the Darknet",
  "client": "Sgt Mustman",
  "artefactdescription": "BragBook Flair"
}
```

Placeholder names are casesensitive.

If you want to use one of the included placeholders place it as attribute value for the collectors defined in the instructions xml file you want to use, like seen in the [above example](#placeholders).

You can provide your own placeholders file by using the [cli argument '-g'](#placeholder-file).

## Collectors

mosk does its collection through collectors. There are already several collectors implemented:

### Supported collectors
#### Scope 'localhost'
* ShellHistoryOfAllUsers (macOS)
* LocalTime (macOS)
* NVRAMCollector
* FileContent
* [FileCopy (macOS, Linux)](#filecopy) 
* [FileMetadata](#filemetadata)
* <a href="#localhost-filehash">FileHash</a>
* FileExistence
* MachineName
* OSName (macOS)
* OSVersinon (macOS)
* OSTimezone
* SudoVersion (macOS)
* OSPlatform
* NVRAMCollector (macOS)
* DetectFusionDrive (macOS)
* DetectFileFault (macOS)
* DetectFileByName (macOS)
* InstalledApplications (macOS)
* FileSystemInformation (macOS)
* [HardwareInformation (macOS)](#hardwareinformation)
* [AllUsernames (macOS, Linux)](#allusernames)
* CurrentUser
* [RecentUserItems (macOS)](#RecentUserItems)
* [PLUtil (macOS)](#PLUtil)

##### RecentUserItems
Uses the external cli command 'mdfind' with certain filters to collect the recently 
opened files by a user in her or his homefolder. Recently means, in the last 60 Minutes.

```xml
<RecentUserItems module="artefact.localhost.user" 
                 mdfind_path="./external_tools/mdfind" />
```
The above example uses the `mdfind` command of the machine the collector is running on. You can provide your own
copy of the command by defining the parameter `mdfind_path`. Along side of your own copy of the command you also
have to provide a text file containing the md5-hash of the copy. The md5-file has to be named like the copied
command with the extension `.md5`, so in this case `mdfind.md5`.

You can also not provide the parameter `mdfind_path`, then the `mdfind` cli command of the live running machine
is used instead.

##### PLUtil
Uses the external cli command `plutil` with the parameter `-p` to collect the conent of a .plist-file provided
by the collector parameter `source_path`.

```xml
<PLUtil module="artefact.localhost.tools" 
        source_path="~/Library/Preferences/com.apple.Dock.plist" />
```
The above example uses the `plutil` command of the machine the collector is running on. You can provide your own
copy of the command by defining the parameter `tool_path`. Along side of your own copy of the command you also
have to provide a text file containing the md5-hash of the copy. The md5-file has to be named like the copied
command with the extension `.md5`, so in this case `plutil.md5`.

```xml
<PLUtil module="artefact.localhost.tools" 
        source_path="~/Library/Preferences/com.apple.Dock.plist" 
        tool_path="<Your Tools Folder>/plutil" />
```

##### AllUsernames
Allowed attributes/parameters:

*properties*

*users_with_homedir*<br/>
'True' or 'False', if true only users with user folders are been collected.

##### FileCopy
Copies files from the target to a definable target directory, where it will create a uniquely named subdirectory.

```xml
<FileCopy module="artefact.localhost.file" 
          source_path="/users/testuser/test.txt" />
```
This would copy the file `/users/testuser/test.txt` into the folder under which mosk is been executed inside a new 
subdirectory, for example named `test.txt_2021010112120001`, where there is a timestamp incorporated, and a counter 
at the end of the subdirectories name.

You can provide more than one file to copy by separating each file path with a `\n`, 
for example `/filepath1\n/filepath2`.

FileCopy can also copy file trees. As source you have to provide the source
directory. You can also provide a source path with wildcard characters in 
the leaf, for example `/somepath/*path` for all directories which end with
`path`, or `/somepath/*` for all directories in `somepath`.

##### FileMetadata
Collectes metadata of a file by harnessing Python default modules:
* os.path

Metadata collected:
* Create Date and Time in UTC
* Modifed Date and Time in UTC
* Last Accessed Date and Time in UTC
* Birth Date and Time in UTC
* Size in Bytes
* Number of used Blocks
* Block Size
* INode Number
* Owner ID
* Group ID
* Filetype and Permissions

Example:
```xml
<FileMetadata module="artefact.localhost.file" 
              source_path="/usr/somefile" />
```
##### <a name="localhost-filehash"></a>FileHash 
Calculates the hash of a provided file and compares it against a 
provided MD5 hash using businessclass.support.md5() to calculate
the MD5 hash.

Example:
```xml
<FileHash module="artefact.localhost.file" 
          source_path="sometestfile.txt" 
          filehash="0db7d1adf349b912f612c9be06278706"/>
```

##### HardwareInformation
Will use the command `system_profiler` to collect hardware information similar 
to the info you get, when opening "About this Mac".

The following information will be collected:
* Model Name
* Model Identifier
* Chip
* Total Number of Cores
* Memory
* System Firmware Version
* OS Loader Version
* Serial Number
* Hardware UUID
* Provisioning UDID
* Activation Lock Status

#### Scope 'Internet'
* ExternalLinksOnUrl
* TemperatureFromOpenWeatherDotCom
* TimeFromNTPServer

#### Scope 'network'
* TemperatureFromOpenWeatherDotCom
* ExternalLinksOnUrl
* TimeFromNTPServer

#### Scope 'EWFImage'
* FolderInformation (macOS, Linux)
* ImageMetadata (macOS, Linux)
* PartitionTable (macOS, Linux) 
* File (macOS, Linux)
* <a href="#image-filehash">FileHash (macOS, Linux)</a>
* CompleteFileSystemInfo (macOS, Linux)

##### <a name="image-filehash"></a>FileHash
Calculates the hash of a provided file inside of a image file and compares it against a 
provided MD5 hash using businessclass.support.md5() to calculate
the MD5 hash.

```xml
<FileHash module="artefact.image.file" 
          source_path="/08 Email/eml/" 
          filename="68E31B21-00033004.eml"
          filehash="ae797b8a31413cb96fde720488a4ec0e" />
```

#### Scope 'Debug'
* DebugPlaceholder

## CLI Arguments
Run mosk:

```
./mosk -i ./examples/collect-test.xml
```

The only required argument is '--instructions', or '-i' followed by the path to the [instructions file](#instructions).

Additional arguments are:

#### Examiner
```
-a <examiner>
```

#### Debug Level
```
-l [DEBUG|INFO|WARN|ERROR|CIRITICAL]
```

#### Placeholder file
```
-g <placeholder file path>
```
By default this is 'global_placeholders.json'.

#### Protocol Log File
```
-p <Custom Protocol Log File path>
```
Use this to create your own protocol log file instead of going with the log files automatically created by mosk.

#### Help
````
--help
````
Get a short description of the script parameters.
## Providing automatic documentation
As described in the introduction, mosk should provide some layer of documentation of the "what", "when" and "how". Big part (if not all) of the "how" is currently placed inside the resource files for the text strings. Per default only *resources/collector_text_None.json* is provided and you have to translate or modify it yourself to provide the documentation in your language, or if you need a more detailed explanation what a collector did. Currently the collector documentation is very rudimenatry for the sake of speed of development.

## Dependencies

The folder `dependencies` contains text files which describe the dependencies for the collectors, 
`minimum-dependencies.txt` which describes the bare minimum of external python modules you have to install in order
to run a minimum `mosk` instruction-collection. You can use these files to automatically install the dependencies with
the following command:

```
pip install -r <dependencies text file>
```

NOTE:
Not all collectors in a collector module needs to be tested independently. Reason is, that Python needs to load
the external modules upon instatiating any of the collectors in a collectors module. So if any of the import statements
at the beginning is raising an exception you can assume, that the collector cannot be used. Of course, there may
be edge cases, where this is not true. But assume you have to install all external modules, which are being imported
at the beginning of a collector module.

<span style="color:red">
NOTE on collectors for image files:
You will have to provide your own image file for these tests. This project currently does not include a demo
image file. So, when running the dependency tests for image collector modules, you will run into exceptions.
</span>

## Protocol

mosk will try to write a protocol of the collection process. Every collector for that reason will collect not only the data but also metadata. The following metadata may be collected:

* File path
* MD5 hash of collected data
* Collection timestamp (will always be collected)

If not possible or not suitable, the above metadata will not be collected.

Additionally it will log the name of the collector class and all provided parameters to the collector. This can be used to, for example log some description for why the data has been collected in the first place.

### Log File Protocol

The log file protocol writer will write a collection log in a pure text file.

#### Example

The following instrcutions ...

```xml
<Task>
    <TaskHeader>
        <examiner title="Examiner">
            sho
        </examiner>
        <originaltask title="Assignment">
            Some task
        </originaltask>
        <taskissuer title="Client">
            Sgt Mustman
        </taskissuer>
        <artefactdescription title="Description of Artefact">
            MacBook Flair
        </artefactdescription>
        <taskdescription title="Task Description">
            Some task description
        </taskdescription>
    </TaskHeader>
    <Instructions>
        <Root module="source.root">
           <LocalHost path="!@machinename@!" module="source.localhost">
                <OSTimezone module="artefact.localhost.osinformation" />
                <FileContent module="artefact.localhost.file" 
                             source_path="~/tests/test.txt"
                             description="Collected the content of the file for demo purposes." />
            </LocalHost>
            <Network module="source.network">
                <TimeFromNTPServer module="artefact.network.system" />
            </Network>
        </Root>
    </Instructions>
</Task>
```

... will lead to a protocol like the following.

```txt
****************
Collection Start
****************
2021-03-23 06:29:16.830065
Clerk: 
            sho
        
Task: 
            Some task
        
Client: 
            Sgt Mustman
        
Artefact Description: 
            MacBook Flair
        
Task Description: 
            Some task description
            

*********************************
Root:0->LocalHost:1->OSTimezone:2
*********************************
Title: OS Timezone
Description: Collect the local timezone by using the Python module datetime.
Collection Method: datetime.now astimezone
 
-- Collection Data     ----------

CET

-- Collection Metadata ----------

Collection Time Stamp: 2021-03-24 14:52:25.861043

Collector: OSTimezone

---------------------------------


 
**********************************
Root:0->LocalHost:1->FileContent:2
**********************************
Title: File content collector
Description: Uses the python file context manager to open the file in read mode and store its
content and a MD5 hash of its content.
Collection Method: python file context manager
 
-- Collection Data     ----------

This is a test file.

It should be used to test
working with file content.

-- Collection Metadata ----------

Collection Time Stamp: 2021-03-24 14:52:25.905901
Source MD5: 0db7d1adf349b912f612c9be06278706
Source path: /User/AUser/tests/test.txt

Collector: FileContent
filepath: '~/tests/test.txt'
description: 'Collected the content of the file for demo purposes.'

---------------------------------
         
            
**************
Collection End
**************
2021-03-23 06:34:15.365227
```

### Enable ewf image collectors

To use the ewf collectors you need to install pytsk3 and libewf-python.

## Install pytsk3

You can get pystk3 from its [github repository](https://github.com/py4n6/pytsk).

Nothing special to consider here. Just install it with `pip`:

```
pip install pytsk3
```

### Install libewf-python

For libewf you first have to grep it from its [github repostory](https://github.com/libyal/libewf/releases).
Then you have to build your install package in the local libewf folder:

```
sudo python setup.py build
```

When that is done, install it with the setup script like so:

```
sudo python setup.py install
```

# REMINDER

This is currently mostly a training project for me. After all, I am new to Python. Don't expect to much usefullness out of it until further notice ;-)
