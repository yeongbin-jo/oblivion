#! -*- coding=utf-8 -*-
'''
Created on 2013. 5. 13.

@author: YEONGBIN
'''

from pcapy import open_live
from pcapy import findalldevs
from HexByteConverter import ByteToHex
import urllib
import urllib2
import wx
from threading import Thread
import socket
import sys
from struct import unpack

TRAY_TOOLTIP = u'망각 모니터'
TRAY_ICON = 'horn.ico'


class SniffThread(Thread):
    def __init__(self, dev):
        self.dev = dev
        Thread.__init__(self)

    def run(self):
        reader = open_live(self.dev, 65536, 0, 10000);
        reader.setfilter('port 11020 or port 11021 or port 11023')
        reader.loop(-1, process_packet)

def heartbeat(ch):
    if ch != '':
        try:
            req = urllib2.Request("http://oblivion.drunkenhaze.org/rest/alive/%s" % (ch))
            urllib2.urlopen(req)
        except:
            print("Heartbeat failed")

def getChannelFrom(ip, port):
    if ip == "211.218.233.210":
        if port == "11020":
            return "1"
        elif port == "11021":
            return "2"
    elif ip == "211.218.233.211":
        if port == "11020":
            return "3"
        elif port == "11021":
            return "4"
        elif port == "11023":
            return "5"
    elif ip == "211.218.233.212":
        if port == "11020":
            return "6"
        elif port == "11021":
            return "7"
        elif port == "11023":
            return "8"
    elif ip == "211.218.233.213":
        if port == "11020":
            return "9"
        elif port == "11021":
            return "10"
        elif port == "11023":
            return "12"
    elif ip == "211.218.233.214":
        if port == "11020":
            return "13"
        elif port == "11021":
            return "14"
        elif port == "11023":
            return "15"
    elif ip == "211.218.233.215":
        if port == "11020":
            return "16"
        elif port == "11021":
            return "17"
        elif port == "11023":
            return "18"
    else:
        return ""

def parse_payload(payload):
    FIELDBOSS_SIGNATURE = "\x03\x00\x01\x01\x06\x00"
    result = {}

    if FIELDBOSS_SIGNATURE in payload:
        start = payload.find(FIELDBOSS_SIGNATURE) + len(FIELDBOSS_SIGNATURE) + 1
        end = start + ord(payload[start - 1]) - 1
        if end <= len(payload):
            try:
                parsed = payload[start:end].decode('utf-8')
                if u"나타났다" in parsed:
                    result['type'] = 'appear'
                    result['target'] = parsed[parsed.find(u"에") + 2:parsed.find(u"나타났다") - 2].strip()
                elif u"쓰러뜨리셨습니다" in parsed:
                    result['type'] = 'finish'
                    result['target'] = parsed[:parsed.find(u"님이")].strip()
            except:
                print("Parse fail: [%s]" % (ByteToHex(payload)))
    return result

def parse_packet(packet):
    eth_length = 14
    
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
    
    if eth_protocol == 8 :
        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20+eth_length]
         
        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
        version_ihl = iph[0]
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])
        
        if protocol == 6 :
            t = iph_length + eth_length
            tcp_header = packet[t:t+20]
 
            #now unpack them :)
            tcph = unpack('!HHLLBBHHH' , tcp_header)
             
            source_port = tcph[0]
            dest_port = tcph[1]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4
            h_size = eth_length + iph_length + tcph_length * 4
            data = packet[h_size:]
            return (s_addr, d_addr, source_port, dest_port, data)

def process_packet(hd, data):
    ip, _, port, _, payload = parse_packet(data)
    channel = getChannelFrom(ip, str(port))

    if "\x88\x0A\x00\x00\x00\x01" in payload:
        heartbeat(channel)

    result = parse_payload(payload)
    if result:
        print(result)
        try:
            req = urllib2.Request("http://oblivion.drunkenhaze.org/rest/%s/%s/%s" % (result['type'],  #@IndentOk
	                                    urllib.quote(result['target'].encode('utf-8')),
	                                    channel),
	                              "")
            urllib2.urlopen(req)  #@IndentOk
        except:
            print("Server Error")

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        #create_menu_item(menu, 'Say Hello', self.on_hello)
        #menu.AppendSeparator()
        create_menu_item(menu, u'종료하기', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        pass

    def on_hello(self, event):
        pass

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)

def main():
    try:
        for dev in findalldevs():
            SniffThread(dev).start()
        app = wx.PySimpleApp()
        TaskBarIcon()
        app.MainLoop()
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
