#mosk

mosk is a short form for "macOS Kraken". Originally created as framework to collect artefacts from macOS images and machines running macOS. The framework is designed to be easyly extensible.

mosk should not only run collectors to collect artefacts, it should also provide some layer of documentation of what has been collected and how this happend, to be able to later explain the "what" and the "who" to others, for example in court.

##Instructions

To run mosk you have to provide instructions provided, for example, as XML files.

###Example Instruction XML
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
                <HostsRegisteredInFritzBox module="artefact.network.router" address="10.0.0.1" port="48000" encrypt="False"/>
            </Network>
        </Root>
    </Instructions>
</Task>
```

As instructions format currently only XML is supported.

###Placeholders

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

###'global_placeholders.json'

You can provide placeholders in a global placeholder file, by default "global_placeholders.json":

```json
{
  "examiner": "sho",
  "clienttask": "Do something, dam it!",
  "client": "Sgt Mustman",
  "artefactdescription": "BrackBook Flair",
  "APIKey": "a3f2a8f1fff851cds90a0cd7aef46389",
  "FritzIP": "10.0.99.254",
  "FritzPort": "38999"
}
```

If you want to use one of the included placeholders place it as attribute value for the collectors defined in the instructions xml file you want to use, like seen in the [above example](#placeholders).

You can provide your own placeholders file by using the cli argument '-e'.

##Collectors

mosk does its collection through collectors. There are already several collectors implemented:

###Currently supported collectors
####Scope 'localhost'
AllUsernames
CurrentUsername
FileExsistence
FileContent
MachineName
OSName
OSVersion
OSTimezone
SudoVersion

####Scope 'localhost.mac'
ShellHistoryOfAllUsers
LocalTime
NVRAMCollector

####Scope 'network'
TemperatureFromOpenWeatherDotCom
ExternalLinksOnUrl
HostsRegisteredInFritzBox
TimeFromNTPServer
    
