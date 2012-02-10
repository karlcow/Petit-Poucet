#!/usr/bin/env python2.7
# encoding: utf-8
"""
pathcolor.py

Created by Karl Dubost on 2012-02-09.
Copyright (c) 2012 Grange. All rights reserved.
Licensed under the MIT license: http://www.opensource.org/licenses/MIT
"""
import argparse, sys, re, os
import email
from PIL import Image, ImageDraw
side = 20
size = side, side

def parse_received(journey):
    """Parse the Received header to extract meaningful information
    http://tools.ietf.org/html/rfc5336#section-3.7.3
    Received: 
    from someone.local (machine.example.com [1.2.3.4]) (authenticated bits=0) 
    by smtp.example.net (blabla) 
    with ESMTP id q1234567x123456 (blabla) 
    for <mailing@list.example.org>; 
    Thu, 9 Feb 2012 18:34:09 GMT
    """
    IPpattern = re.compile(r'.*\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\].*')
    iplist = []
    for stop in journey:
        try:
            ip = IPpattern.match(stop)
            iplist.append(ip.groups()[0])
        except:
            pass
    return iplist
    
def ip2color(ip):
    """take an ip address such as 100.150.200.45
    and convert it to a rgb color string with opacity
    rgb(100,150,200,45./255.)
    """
    ipvalues = ip.split(".")
    return (int(ipvalues[0]),int(ipvalues[1]),int(ipvalues[2]),int(ipvalues[3]))

def ip2trail(ips):
    """Take the list of colors and make a badge"""
    badgeLength = len(ips)*side
    img = Image.new("RGBA", (badgeLength,side), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    n=0
    color = (0,0,0,0)
    for ip in ips:
        color = ip2color(ip)
        draw.rectangle( ((n*side,0),((n+1)*side,side)),  fill=color )
        n=n+1
    return img

def main():

    # Parsing arguments from the CLI
    parser = argparse.ArgumentParser(description="Find the IP address of the Email Sender")
    parser.add_argument('emailfile', metavar='FILE', help='email file to be processed', action='store', nargs=1, type=argparse.FileType('rt'))
    args = parser.parse_args()
    mailfile = args.emailfile[0]
    filename = os.path.basename(mailfile.name)

    # Parsing the email
    msg = email.message_from_file(mailfile)
    journey = msg.get_all('Received')
    # Reverse the list
    journey.reverse()
    iplist = parse_received(journey)
    # iplist[0] is the Sender
    stonetrail = ip2trail(iplist)
    # stonetrail.show()
    stonetrail.save(filename+".png", "PNG")
    
    
if __name__ == "__main__":
    sys.exit(main())
