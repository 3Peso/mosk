# mosk

mosk is a short form for "macOS Kraken". Originally created as framework to collect artefacts from macOS images and machines running macOS. The framework is designed to be easyly extensible with additional collector classes.

mosk should not only run collectors to collect artefacts, it should also provide some layer of documentation of what has been collected and how this happend, to be able to later explain the "what", "when" and the "how" to others.

## Instructions

To run mosk you have to provide instructions provided, for example, as XML files.

### Example Instruction XML
```xml
<Task>
    <TaskHeader>
        <examiner title="Sachbearbeiter">
            !@examiner@!
        </examiner>
        <originaltask title="Auftrag">
            !@clienttask@!
        </originaltask>
        <taskissuer title="Auftraggeber">
            !@client@!
        </taskissuer>
        <artefactdescription title="Beschreibung des Asservats">
            !@artefactdescription@!
        </artefactdescription>
        <taskdescription title="Beschreibung der Aufgabe">
            Wie lauten die Eckdaten des Betriebssystems des zugrundeliegend Artefakts?
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
                <LocalTime module="artefact.localhost.mac.system" />
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

### Placeholders

You can define placeholders inside the instructions enclosed by '!@' '@!', for example '!@test@!. mosk will try to fill in the "blanks" in two runs. First run is before the actual collectors are been instanciated. You can provide the values for this in the file 'global_placeholders.json'. Second run actually happens during collection. If one collector collects the value for the placeholder before another collector consumes it.

Currently only XML is supported as instructions format. So currently the only way to provide values for placeholders collected by collectors is by providing the attribute "placeholdername" for the collector which should collect the value for later use.
Example:

```xml
            <LocalHost module="source.localhost">-->
                <MachineName module="artefact.localhost.machineinformation" placeholdername="machinename" />
            </LocalHost>
            <LocalHost path="!@machinename@!" module="source.localhost">
              ...
            </LocalHost>
```
The above example also implies that you can reuse placeholders throught the instructions as often as you want, as long as they already have been intiailzed before usage.

### 'global_placeholders.json'

You can provide placeholders in a global placeholder file, by default "global_placeholders.json":

```json
{
  "examiner": "sho",
  "clienttask": "Do something, dam it!",
  "client": "Sgt Mustman",
  "artefactdescription": "BrackBook Flair"
}
```

If you want to use one of the included placeholders place it as attribute value for the collectors defined in the instructions xml file you want to use, like seen in the [above example](#placeholders).

You can provide your own placeholders file by using the [cli argument '-g'](#placeholder-file).

## Collectors

mosk does its collection through collectors. There are already several collectors implemented:

### Supported collectors
#### Scope 'localhost'
AllUsernames
CurrentUsername
FileExsistence
FileContent
MachineName
OSName
OSVersion
OSTimezone
SudoVersion

#### Scope 'localhost.mac'
ShellHistoryOfAllUsers
LocalTime
NVRAMCollector

#### Scope 'network'
TemperatureFromOpenWeatherDotCom
ExternalLinksOnUrl
HostsRegisteredInFritzBox
TimeFromNTPServer

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
