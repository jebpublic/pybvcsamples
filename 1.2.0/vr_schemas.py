#!/usr/bin/python

"""
Copyright (c) 2015,  BROCADE COMMUNICATIONS SYSTEMS, INC

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
 are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""

import sys
import time
import json
import pybvc
import os
import re


from pybvc.netconfdev.vrouter.vrouter5600 import VRouter5600
from pybvc.common.status import STATUS
from pybvc.controller.controller import Controller
from pybvc.common.utils import load_dict_from_file, progress_wait_secs




def cleanup(line):
    line = line.replace('"// vi: set smarttab et sw=4 tabstop=4:',"")
    line = line.replace("\\n",'\n')
    line = line.replace("\\t",'\t')
    line = line.replace("\\r",'\r')
    line = line.replace('\\\"','\"')
    line = line.replace('\\"','\"')
    line = line.replace('\"','\"')
    #line = line.replace('"module','module')
    #line = line.replace('"/*','/*')
    #line = line.replace('}"$','}')
    line = re.sub('^"module','module', line)
    line = re.sub('^"/*','/*', line)
    line = re.sub('\}"$', '}', line)
    return line


def main():
    f = "vr_cfg.yml"
    d = {}
    if(load_dict_from_file(f, d) == False):
        print("Config file '%s' read error: " % f)
        exit()

    try:
        ctrlIpAddr = d['ctrlIpAddr']
        ctrlPortNum = d['ctrlPortNum']
        ctrlUname = d['ctrlUname']
        ctrlPswd = d['ctrlPswd']

        nodeName = d['nodeName']
        nodeIpAddr = d['nodeIpAddr']
        nodePortNum = d['nodePortNum']
        nodeUname = d['nodeUname']
        nodePswd = d['nodePswd']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 0
    
    print ("\n")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print ("<<< 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    
    
    print ("\n")
    time.sleep(rundelay)    
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("<<< '%s' added to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result[0]
    if(status.eq(STATUS.NODE_CONNECTED) == True):
        print ("<<< '%s' is connected to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    
    print "\n"
    print ("<<< Get list of YANG models supported by " + nodeName)
    time.sleep(rundelay)
    result = vrouter.get_schemas()
    status = result[0]
    if(status.eq(STATUS.OK)):
        print "YANG models list:"
        slist = result[1]
        print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief())        
        exit(0)
    

    directory = "vr_schema_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    print "\n"
    print ("<<< For each YANG model retreive its YANG schema")
    for aModel in result[1]:
        moduleName =aModel['identifier'] 
        theSchema = vrouter.get_schema(aModel['identifier'], aModel['version'])
        status = theSchema[0]
        if(status.eq(STATUS.OK)):
            slist = theSchema[1]
            print json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            schema = cleanup(json.dumps(slist, default=lambda o: o.__dict__, sort_keys=True, indent=4))
            moduleFileName = directory + "/" + moduleName + ".yang"
            print "Writing " + moduleFileName
            f = open(moduleFileName, 'w')
            f.write(schema)
            f.close()
        else:
            continue

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


if __name__ == "__main__":
    main()
