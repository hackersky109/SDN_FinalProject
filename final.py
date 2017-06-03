"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI
import os


class MyTopo( Topo ):

    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts h1~h16
        """
        self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        self.addHost('server1', ip='10.0.0.3', mac='00:00:00:00:00:03')
        self.addHost('server2', ip='10.0.0.4', mac='00:00:00:00:00:04')
        """
        self.addHost('h1', ip='0.0.0.0')
        self.addHost('h2', ip='0.0.0.0')
        self.addHost('server1', ip='0.0.0.0')
        self.addHost('server2', ip='0.0.0.0')
        # Add Switches
        self.addSwitch('s1')

        # Add links
        self.addLink('s1', 'h1')
        self.addLink('s1', 'h2')
        self.addLink('s1', 'server1')
        self.addLink('s1', 'server2')

def perfTest() :
    "Create network and run simple performance test"
    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    #net.addController("ryu", controller=RemoteController, ip="192.168.2.48")
    net.addController("ryu", controller=RemoteController, ip="127.0.0.1")
    net.start()
    '''
    print "-----Dumping host connections-----"
    dumpNodeConnections(net.hosts)
    print "-----Testing pingFull-----"
    net.pingFull()
    h1, h2, h16 = net.get('h1', 'h2', 'h16')
    print "-----Setting iperf server  with h1-----"
    h1.cmdPrint('iperf -dds -u -i 1 &')
    print "-----Setting iperf server  with h16-----"
    h16.cmdPrint('iperf -s -u -i 1 &')
    print "-----h2 connect to h1-----"
    h2.cmdPrint('iperf -c'+h1.IP()+' -u -t 10 -i 1 -b 100m')
    print "-----h2 connect to h16-----"
    h2.cmdPrint('iperf -c'+h16.IP()+' -u -t 10 -i 1 -b 100m')
    '''
    server1, server2= net.get('server1', 'server2')
    os.popen('ovs-vsctl add-port s1 enp0s8')
    server1.cmdPrint('dhclient '+server1.defaultIntf().name)
    server2.cmdPrint('dhclient '+server2.defaultIntf().name)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()

topos = { 'mytopo': ( lambda: MyTopo() ) }
