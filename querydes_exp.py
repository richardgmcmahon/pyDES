#!/usr/bin/python
"""Reads an input file and submits a query to the WSA archive.

Example input file:
    
select top 10 from lassource where ra>140 and ra<240
    
"""

"""
TODO needs some 

support for fits, etc on command line
unzip the fits

Original by EGS in 
20051216; rgm added fits support (hardwired it)
20051216; rgm forced the output to be written to /tmp
20090409; rgm added DB support as input
20090409; rgm added emailaddress support as input


TODO 
option to specify the output filename
option to specify fits or csv on the command line

"""
import os, sys, re, string, time
import urllib, urllib2, cookielib

# import the optparse library to ease command line options
from optparse import OptionParser

now = time.localtime(time.time())
print 'Current time: ',time.strftime("%Y-%m-%d %H:%M:%S %Z", now)
date=time.strftime("%Y%m%d", now)
print 'day: ',date
print 'Current working directory: ',os.getcwd()
print 'Executing: ',sys.argv[0]

usage = "usage: %prog [options] sqlfile"
parser = OptionParser(usage)

#parser = OptionParser()


parser.add_option("-i", "--input", dest="input", help="input sql file")
parser.add_option("-q", "--query", dest="query", 
 help="specify query on the command line")
parser.add_option("-f", "--format", dest="format", default='html',
 help="Output format (csv/fits/html) [Default: %default]")
parser.add_option("-o", "--output", dest="output",  help="Output filename")
parser.add_option("-e", "--email", dest="email", 
 default='rgm@ast.cam.ac.uk',
 help="Email address for results of long queries [Default: %default]")
parser.add_option("-d", "--db", dest="db", default='UKIDSSDR5PLUS',
help="UKIDSS Database to use [Default: %default]")

(options, args) = parser.parse_args()

if args==[]:
    parser.error("There is no input query file.")

# Get the input file name from disk
infile=args[0]
assert os.access(infile, os.F_OK), "File not found: "+infile

query = open(infile,'r').read()

#fquery=filtercomment(query)
#query=fquery


#http://dbweb4.fnal.gov:8080/DESQE/app/run?dbname=des_exposure
#&sql_statement=select
#&output_type=text,
#&maxrows=1000&
#&submit=Run


# This is the base query.
dd={'dbname': 'des_exposure', 
    'sql_statement': query, 
    'output_type': 'text,',
    'submit': 'Run'}

url="http://dbweb4.fnal.gov:8080/DESQE/app/run?"


basequery=url + urllib.urlencode(dd)

print 'basequery: ',basequery

t0 = time.time()
res=opener.open(basequery).read()
print 'Elapsed time(secs): ',time.time() - t0 
htmlresult = "/tmp/wsa_freeform_result.html"
f=open(htmlresult, 'w')
f.write(res)
f.close()
print "%s file saved" % htmlresult

# Look for the csv/fits link
csvfile=re.compile("<a href=\"(\S+%s).+" % options.format).search(res).group(1)
# Request the csvfile
csvres=opener.open(csvfile).read()
# Save file to local disk
if options.output:
    localcsv = options.output
else:
    localcsv = "/tmp/"+csvfile.split('/')[-1]
   
f=open(localcsv, 'w')
f.write(csvres)
f.close()

print "%s file saved" % localcsv

print 'Elapsed time(secs): ',time.time() - t0 










