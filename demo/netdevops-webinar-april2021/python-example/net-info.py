#!/usr/bin/env python
#
# Example: Arista eAPI script to pull info from all nodes in the network
#
from jsonrpclib import Server
import ssl

# Ignore SSL connection warnings from self-signed certificates on Lab switches
try:
  _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
  pass
else:
  ssl._create_default_https_context = _create_unverified_https_context

# Vars
# Example Node List, Modify to make it your own

nodes = ["172.31.0.11",
         "172.31.0.12",
         "172.31.0.14",
         "172.31.0.15",
         "172.31.0.30"]

# Modify switch login userid and pw as needed
userid = "admin"
password = "admin"


print ("\n")
print ("Network Inventory")
print ("---------------------------------------------------------------------------------------------------------------------")
print ("Node       IP Address      Serial No     Model                Uptime(s)    TotalMem   FreeMem    Version    Neighbors ")
print ("---------------------------------------------------------------------------------------------------------------------")

# Loop through each node and gather info

for node in nodes:

   # Instantiate switch object on each node
   RESTURL = "https://" + userid + ":" + password + "@" + node + "/command-api"
   switch = Server(RESTURL)

   # run command(s) against switch object
   # list of command output returned in a List (array) or JSON key:value pairs
   response = switch.runCmds(1, ["show hostname",
                                 "show version",
                                 "show ip interface Management1",
                                 "show lldp neighbors"])

   hostname = response[0]["hostname"]
   serialNo = response[1]["serialNumber"]
   model = response[1]["modelName"]
   totalMem = response[1]["memTotal"]
   freeMem = response[1]["memFree"]
   eosVersion = response[1]["version"]
   uptime = response[1]["uptime"]
   mgmtip = response[2]["interfaces"]["Management1"]["interfaceAddress"]["primaryIp"]["address"]
   lldpNeighbors = response[3]["lldpNeighbors"]
   numLldpNeighbors = len(lldpNeighbors)

   print ("%-10s %-15s %-13s %-20s %-12s %-10s %-10s %-10s %-10s" % (hostname, mgmtip, serialNo, model, uptime, totalMem, freeMem, eosVersion, numLldpNeighbors))

# end of loop

print ("\n")