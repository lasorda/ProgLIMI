#!/bin/bash/env python
#-*- coding: utf-8 -*-
"""
Simple example of setting network and CPU parameters
NOTE: link params limit BW, add latency, and loss.
There is a high chance that pings WILL fail and that
iperf will hang indefinitely if the TCP handshake fails
to complete.
"""

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import CPULimitedHost, RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

from random import random
    
class MyTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        from readtopo import readtopo
        monitors, SDN_node, paths, links= readtopo()

        # Add hosts and switches
        switches = {}
        for l in links:
            #if node not exist, create it
            if not switches.has_key( l[0] ):
                switches[ l[0] ] = self.addSwitch("s%s"%l[0])
            if not switches.has_key( l[1] ):
                switches[ l[1] ] = self.addSwitch("s%s"%l[1])
            #add link of nodes
            delay = (int(l[0]) + int(l[1]))%10 + 1
            loss = (int(l[0]) + int(l[1]))%5 + 1
            # self.addLink(switches[l[0]], switches[l[1]], delay="%.2fms"%delay, loss=loss)
            # print "%2s"%l[0], '->', "%2s"%l[1], "delay:%2s"%delay, "loss:%2s"%loss
            self.addLink(switches[l[0]], switches[l[1]], delay="%.2fms"%delay)

        #nodes to send and receive probe packet
        nodes = []
        for x in monitors:
            if x not in SDN_node:
                nodes.append(x)
        nodes.append(SDN_node[0])

        switches[ 'r'] = self.addSwitch('r%d'%(len(switches)+1))
        for k in nodes:
            self.addLink(switches[k], switches['r'])

        #create host
        h1 = self.addHost('h1')
        self.addLink(switches['r'], h1)
        
        # h2 = self.addHost('h2')
        # h3 = self.addHost('h3')
        # h4 = self.addHost('h4')
        # h5 = self.addHost('h5')
        
        # self.addLink(switches[1], h3)
        # self.addLink(switches[4], h4)
        # self.addLink(switches[5], h5)

def main():
    "Create network and run simple performance test"
    topo = MyTopo(n=4)
    net = Mininet(topo=topo, build = False, link=TCLink)
    c0 = RemoteController( 'c0', ip='0.0.0.0' )
    net.addController(c0)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()