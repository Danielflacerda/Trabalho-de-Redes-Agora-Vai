#!/usr/bin/python   
#coding=UTF-8                                                                         
                                                                                        
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopology(Topo):
    def __init__(self,**opts):
        # Inicializando a topologia e configurações padrões
        Topo.__init__(self, **opts)
        #Adiciona os switchs do 1 ao 3 a topologia.
        switch = self.addSwitch('switch1')
        switch = self.addSwitch('switch2')
        switch = self.addSwitch('switch3')

        #Adiciona hosts do 1 ao 9 na topologia.
        for h in xrange(9):
            host = self.addHost('host%d' % (h + 1))

        #Adicionando links dos switchs
        self.addLink('switch1', 'switch2')
        self.addLink('switch2', 'switch3')
        self.addLink('switch1', 'switch3')
        #Atribuindo 3 hosts a cada switch para criar uma topologia em forma de árvore.
        self.addLink('host1','switch1')
        self.addLink('host2','switch1')
        self.addLink('host3','switch1')
        self.addLink('host4','switch2')
        self.addLink('host5','switch2')
        self.addLink('host6','switch2')
        self.addLink('host7','switch3')
        self.addLink('host8','switch3')
        self.addLink('host9','switch3')

        #Criando hosts e designando os ips/portas, seguindo o padrão apresentado em sala por Lucas
        self.addHost('host1', ip='10.0.1.101/22')
        self.addHost('host2', ip='10.0.1.102/22')
        self.addHost('host3', ip='10.0.1.103/22')
        self.addHost('host4', ip='10.0.2.101/22')
        self.addHost('host5', ip='10.0.2.102/22')
        self.addHost('host6', ip='10.0.2.103/22')
        self.addHost('host7', ip='10.0.3.101/22')
        self.addHost('host8', ip='10.0.3.102/22')
        self.addHost('host9', ip='10.0.3.103/22') #Host9 será o servidor

def main():
    topo = MyTopology()
    net = Mininet(topo = topo, controller = RemoteController) 
    net.start()
    switch1 = net.get('switch1') #Instancia o switch1 da net
    switch2 = net.get('switch2') #Instancia o switch2 da net
    switch3 = net.get('switch3') #Instancia o switch3 da net
    #Função fornecida por Lucas para que não precisemos tratar loops infinitos da rede no broadcast do protocolo ARP, ou seja, os pacotes não ficarem circulando 
    #infinitamente pelos switchs sem chegar ao host destino.
    for i in xrange(9):
        h = net.get('host%d' % (i + 1))
        h.cmd("ip route add default dev %s-eth0" % ('host%d' % (i + 1)))
        for j in xrange(9):
           h_dst = net.get('host%d' % (j+1))
           h.setARP(h_dst.IP(), h_dst.MAC())
    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()