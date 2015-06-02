#!/usr/bin/python3
import os
import sys
from xml.dom import minidom

import http.client
from urllib.parse import urlparse

errors = []

def usage():
    print("Usage: python3 " + sys.argv[0] + " <feedly_export_file>.opml")
    sys.exit(0)


def parse_feed(xmlfile):
    feeds = []
    for _ in range(len(xmlfile)):
        tmp = {}
        if xmlfile[_].getAttribute('type') == "rss":
            tmp[xmlfile[_].getAttribute('text')] = xmlfile[_].getAttribute('xmlUrl')
            feeds.append(tmp)
    return feeds


def check_http_response(url):
    for name, rss in url.items():
        addr = urlparse(rss)
        try:
            conn = http.client.HTTPConnection(addr[1], 80, timeout=3)
            conn.request("HEAD", addr[2])
            res = conn.getresponse()
            if res.status >= 400:
                errors.append(rss)
                print("Name: %s, URL:%s, Error Code:%d" % (name, rss, res.status))
        except http.client.HTTPException:
            errors.append(rss)
        finally:
            conn.close()


def load_xml(filename):
    long_input_file = os.path.realpath(filename)
    try:
        xmldoc = minidom.parse(long_input_file)
        item_res = xmldoc.getElementsByTagName('outline')
    except Exception:
        print("Error parsing xml file")
        sys.exit(1)
    return item_res


def clean_xml(filename, errors):
    xmldoc = minidom.parse(filename)
    doc_root = xmldoc.getElementsByTagName('outline')

    for j in doc_root:
        if j.getAttribute('type') == "rss" and j.getAttribute('xmlUrl') in errors:
            j.parentNode.removeChild(j)
            print("Removing... %s" % (j.getAttribute('xmlUrl')))

    try:
        f = open(filename + "_clean", "w")
        f.write(xmldoc.toxml())
        print("Creating %s_clean file..." % filename)
    except IOError:
        print("Error creating %s_clean file" % filename)
    else:
        f.close()

if len(sys.argv) != 2:
    usage()
else:
    input_file = sys.argv[1]

outlineItems = load_xml(input_file)

results = parse_feed(outlineItems)

print("%d entries found in %s" % (len(results), input_file))

for site in results:
    check_http_response(site)

print("%d wrong entries found" % (len(errors)))

clean_xml(input_file, errors)

sys.exit(0)
