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


from pybvc.controller.controller import Controller
#from framework.controller.openflownode import OpenflowNode
from pybvc.openflowdev.ofswitch import OFSwitch
from pybvc.common.status import STATUS
from pybvc.common.utils import load_dict_from_file


if __name__ == "__main__":

    f = "of_cfg.yml"
    d = {}
    if(load_dict_from_file(f, d) == False):
        print("Config file '%s' read error: " % f)
        exit()

    try:
        ctrlIpAddr = d['ctrlIpAddr']
        ctrlPortNum = d['ctrlPortNum']
        ctrlUname = d['ctrlUname']
        ctrlPswd = d['ctrlPswd']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5

    print ("\n")
    print ("<<< Creating Controller instance")
    time.sleep(rundelay)
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd, None)
    print ("'Controller':")
    print ctrl.brief_json()
    
    
    print ("\n")
    name = "openflow:1"
#    name = "openflow:10195227440578560"
    print ("<<< Get detailed information about ports on OpenFlow node '%s'" % name)
    time.sleep(rundelay)
    ofswitch = OFSwitch(ctrl, name)
    
    result = ofswitch.get_ports_list()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        ports = result[1]
        for port in ports:
            result = ofswitch.get_port_detail_info(port)
            status = result[0]
            if(status.eq(STATUS.OK) == True):
                print ("Port '%s' info:" % port)
                info = result[1]
                print json.dumps(info, indent=4)
            else:
                print ("\n")
                print ("!!!Demo terminated, reason: %s" % status.brief().lower())
                exit(0)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    sys.exit(0)

#    print ("\n")
    result = ofswitch.get_ports_brief_info()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' ports:" % name)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    
    '''
    print ("\n")
    tableid = 0
    result = ofswitch.get_operational_flows(tableid)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' operational flows:" % tableid)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    print ("\n")
    tableid = 0
    result = ofswitch.get_operational_flows_ovs_syntax(tableid, sort=True)
    status = result[0]
    
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' operational flows:" % tableid)
        flist = result[1]
        for f in flist:
            print json.dumps(f)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print ("\n")
    tableid = 0
    result = ofswitch.get_configured_flows(tableid)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' configured flows:" % tableid)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print ("\n")
    tableid = 0
    result = ofswitch.get_configured_flows_ovs_syntax(tableid, sort=True)
    status = result[0]
    
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' configured flows:" % tableid)
        flist = result[1]
        for f in flist:
            print json.dumps(f)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    '''