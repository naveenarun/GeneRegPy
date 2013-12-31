# -*- coding: utf-8 -*-
"""
Version 1.0

Released as of Tue Dec 31, 2013

@author: Naveen Arunachalam
"""

import numpy as np
import matplotlib.pyplot as plt
plt.ion()

#class, methods for transcription factors

class Node:
    def __init__(self, concentration, behavior, alpha = 1):
        self.u = concentration
        self.state = "on"
        self.B = 0 #basal transcription rate
        self.beta = 1 #normal scaling
        self.alpha = alpha #loss rate = degradation + dilution rate
        self.behavior = behavior
        self.next_u = self.u
    def turnon(self):
        self.state = "on"
    def turnoff(self):
        self.state = "off"
    def active_u(self):
        if self.state == "on":
            return self.u
        else:
            return 0
            
class Edge:
    def __init__(self, nodeA, nodeB, k, action):
        self.start = nodeA
        self.end = nodeB
        self.action = action
        self.k = k
    def regulation_function(self):
        K = self.k
        effect = self.action
        u = self.start.active_u()
        if effect=="act":
            return ((u/K)**H)/(1+(u/K)**H)
        if effect=="rep":
            return 1/(1+(u/K)**H)
    
#operations for gates

def fc(edge1, edge2):
    u=edge1.start.active_u()
    K_u=edge1.k
    K_v=edge2.k
    v=edge2.start.active_u()
    if edge1.action=="act":
        return ((u/K_u)**H)/(1+(u/K_u)**H+(v/K_v)**H)
    if edge1.action=="rep":
        return 1/(1+(u/K_u)**H+(v/K_v)**H)

def and_magic(two_edges):
    return two_edges[0].regulation_function()*two_edges[1].regulation_function()
    
def or_magic(two_edges):
    return fc(two_edges[0],two_edges[1])+fc(two_edges[1],two_edges[0])

def search_my_edges(Node, Edges):
    attached = []        
    for Edge in Edges:
        if Edge.end == Node:
            attached.append(Edge)
    return attached

def regulate(Node, Edges, interval):
    if Node.behavior == "single":
        vectors = search_my_edges(Node, Edges)
        if vectors == []:
            contribution = 0
        else:
            contribution = 0
            for i in vectors:
                contribution += i.regulation_function()
    if Node.behavior == "and":
        two_edges = search_my_edges(Node, Edges)
        contribution = and_magic(two_edges) 
    if Node.behavior == "or":
        two_edges = search_my_edges(Node, Edges)
        contribution = or_magic(two_edges)        
    Node_slope = Node.B+Node.beta*contribution-Node.alpha*Node.u
    Node.next_u = Node.next_u+interval*Node_slope

def search(keyword, filename):
    data = open(filename)
    for line in data:
        if keyword in line.split():
            return line.split()[0]
            
def make_nodes(filename):
    data = open(filename)
    for line in data:
        if "Behavior" in line:
            data.next()
            break
    names = []
    nodes = []
    while True:
        datas = data.next().split()
        if datas == []:
            break
        nodes.append(Node(float(datas[1]),datas[2],alpha=float(datas[3])))
        names.append(datas[0])
    return (nodes, names)
    
def findme(short):
    for i in range(len(Names)):
        if Names[i] == short:
            break
    return Nodes[i]
    
def find_tracking(filename):
    data = open(filename)
    lines = []
    for line in data:
        if "TRACK" in line.split():
            lines.append(line.split()[0])
    return lines

    
def make_edges(filename):
    data = open(filename)
    for line in data:
        if "Node1" in line:
            data.next()
            break
    edges = []
    while True:
        datas = data.next().split()
        if datas == []:
            break
        edges.append(Edge(findme(datas[0]), findme(datas[1]), float(datas[2]), datas[3]))
    return edges

def tracking_values(tracked):
    active_us = np.array([[]])
    for i in tracked:
        active_us = np.append(active_us, [[findme(i).active_u()]], axis=1)
    return active_us
    
#parameters
    


filename = raw_input("Input file name? ")


Nodes = make_nodes(filename)[0]
Names = make_nodes(filename)[1]
Edges = make_edges(filename)

H = 2.

switch = findme(search("SWITCH", filename))
switch.turnoff()

monitor = find_tracking(filename)
t = np.linspace(-0.5,10,1000)




#start quotes here


def integrate(t):
    
    values = tracking_values(monitor)
    interval = (t[-1]-t[0])/t.size
    maximum = 5
    
    for i in t[:-1]:
        if i<0:
            switch.turnoff()
        elif i<maximum:
            switch.turnon()
        else:
            switch.turnoff()
        
        for Node in Nodes:
            regulate(Node, Edges, interval)

        for Node in Nodes:
            Node.u = Node.next_u
        
        values = np.append(values, tracking_values(monitor), axis=0)
        
    for i in range(len(monitor)):
        plt.plot(t,values[:,i], label=monitor[i]+"* value")
        plt.legend()
    plt.ylim(ymin=0,ymax=1.3)
    plt.xlim(xmin=t[0],xmax=t[-1])
    
    plt.show()



integrate(t)

