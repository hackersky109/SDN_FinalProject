# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from operator import attrgetter
import time
import json
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.topology.api import get_switch
import Socket_server
from route import urls
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.lib.packet.packet import Packet

from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.ofctl_v1_3 import mod_flow_entry
from ryu.ofproto.ether import ETH_TYPE_IP

from ryu.lib import dpid as dpid_lib
from ryu.lib import stplib
from ryu.lib.packet import udp
from ryu.lib.packet import arp
from ryu.ofproto import ether
from ryu.ofproto import inet
from ryu.lib.packet import tcp

test_name = 'test_app'

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        wsgi = kwargs['wsgi']
        wsgi.register(test,
                      {test_name: self})

        print("=======Socket Server====")
        Socket_server.init('192.168.2.48',8001)


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        print()
        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)


    def api_add_flow(self):
        switch_list = get_switch(self, None)

        print('switch_list')
        print(switch_list)
        print("==========")
        for switch in switch_list:
            datapath = switch.dp
            parser = datapath.ofproto_parser
            ofproto = datapath.ofproto

        match = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,
                                ip_proto=inet.IPPROTO_TCP,
                                ipv4_src='10.0.2.18',
                                tcp_dst=8080)

        actions = [parser.OFPActionSetField(ipv4_dst='10.0.2.17'),
                   parser.OFPActionSetField(eth_dst='00:00:00:00:00:04'),
                   parser.OFPActionOutput(4)]
        self.add_flow(datapath, 100, match, actions)

        # Set Packet header from Server 1 to Server 2 for SYN_ACK
        match = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,
                                ip_proto=inet.IPPROTO_TCP,
                                ipv4_src="10.0.2.17",
                                ipv4_dst="10.0.2.18")
        actions = [parser.OFPActionSetField(ipv4_src='10.0.2.16'),
                   parser.OFPActionSetField(eth_src='00:00:00:00:00:03'),
                   parser.OFPActionOutput(1)]
        self.add_flow(datapath, 150, match, actions)

    def api_delete_flow(self):
        switch_list = get_switch(self, None)
        for switch in switch_list:
            datapath = switch.dp
            parser = datapath.ofproto_parser
            ofproto = datapath.ofproto

        priority1 = 100
        match1 = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,
                                ip_proto=inet.IPPROTO_TCP,
                                ipv4_src='10.0.2.18',
                                tcp_dst=8080)
        actions1 = [parser.OFPActionOutput(1)]
        self.del_flow(datapath, priority1, match1)

        #self.del_flow(datapath, priority1, match1, actions1)

        priority2 = 150
        match2 = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,
                                ip_proto=inet.IPPROTO_TCP,
                                ipv4_src="10.0.2.17",
                                ipv4_dst="10.0.2.18")
        actions2 = [parser.OFPActionOutput(1)]
        #self.del_flow(datapath, priority2, match1, actions1)
        self.del_flow(datapath, priority2, match2)

    def api_add_flow_v2(self):
        switch_list = get_switch(self, None)

        print('switch_list')
        print(switch_list)
        print("==========")
        for switch in switch_list:
            datapath = switch.dp
            parser = datapath.ofproto_parser
            ofproto = datapath.ofproto

        match = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,
                                ip_proto=inet.IPPROTO_TCP,
                                ipv4_src='10.0.2.19',
                                tcp_dst=8080)

        actions = [parser.OFPActionSetField(ipv4_dst='10.0.2.16'),
                   parser.OFPActionSetField(eth_dst='00:00:00:00:00:03'),
                   parser.OFPActionOutput(4)]
        self.add_flow(datapath, 100, match, actions)

        # Set Packet header from Server 1 to Server 2 for SYN_ACK
        match = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,
                                ip_proto=inet.IPPROTO_TCP,
                                ipv4_src="10.0.2.16",
                                ipv4_dst="10.0.2.19")
        actions = [parser.OFPActionSetField(ipv4_src='10.0.2.17'),
                   parser.OFPActionSetField(eth_src='00:00:00:00:00:04'),
                   parser.OFPActionOutput(1)]
        self.add_flow(datapath, 150, match, actions)

    def api_delete_flow_v2(self):
        switch_list = get_switch(self, None)
        for switch in switch_list:
            datapath = switch.dp
            parser = datapath.ofproto_parser
            ofproto = datapath.ofproto

        priority1 = 100
        match1 = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,
                                ip_proto=inet.IPPROTO_TCP,
                                ipv4_src='10.0.2.18',
                                tcp_dst=8080)
        actions1 = [parser.OFPActionOutput(1)]
        self.del_flow(datapath, priority1, match1)

        #self.del_flow(datapath, priority1, match1, actions1)

        priority2 = 150
        match2 = parser.OFPMatch(eth_type=ether.ETH_TYPE_IP,
                                ip_proto=inet.IPPROTO_TCP,
                                ipv4_src="10.0.2.17",
                                ipv4_dst="10.0.2.18")
        actions2 = [parser.OFPActionOutput(1)]
        #self.del_flow(datapath, priority2, match1, actions1)
        self.del_flow(datapath, priority2, match2)
    def del_flow(self,datapath, priority, match):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        mod = parser.OFPFlowMod(datapath=datapath,
                                command=ofproto.OFPFC_DELETE_STRICT,
                                out_port=ofproto.OFPP_ANY,
                                out_group=ofproto.OFPG_ANY,
                                priority=priority,
                                match=match
                                )
        datapath.send_msg(mod)




    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        # if ev.msg.msg_len < ev.msg.total_len:
        #     self.logger.debug("packet truncated: only %s of %s bytes",
        #                       ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
class test(ControllerBase):

    def __init__(self, req, link, data, **config):
        super(test, self).__init__(req, link, data, **config)
        self.Simple_Monitor = data[test_name]

    @route('app', urls.api_delete_flow, methods=['GET'])
    def flow_mod_add(self, req, **kwargs):
        print("GET==========")
        print(self.Simple_Monitor)
        print("==========")
        simple_monitor = self.Simple_Monitor
        simple_monitor.api_delete_flow()

    @route('app', urls.api_add_flow, methods=['GET'])
    def flow_mod_delete(self, req, **kwargs):
        print("GET==========")
        print(self.Simple_Monitor)
        print("==========")
        simple_monitor = self.Simple_Monitor
        simple_monitor.api_add_flow()
    @route('app', urls.api_delete_flow_v2, methods=['GET'])
    def flow_mod_add_v2(self, req, **kwargs):
        print("GET=====v2=====")
        print(self.Simple_Monitor)
        print("==========")
        simple_monitor = self.Simple_Monitor
        simple_monitor.api_delete_flow_v2()

    @route('app', urls.api_add_flow_v2, methods=['GET'])
    def flow_mod_delete_v2(self, req, **kwargs):
        print("GET==v2========")
        print(self.Simple_Monitor)
        print("==========")
        simple_monitor = self.Simple_Monitor
        simple_monitor.api_add_flow_v2()
