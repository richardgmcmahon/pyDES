VERSION="v0.0.1"  # 
"""

Bandmerge DES finalcut single band files

Useage:

prog -h  will list the options


"""

import sys
import time

import atpy
import asciitable

import pyfits
import copy

#from plotid import *

# might not be needed
import numpy as np

# use native matplotlib or matplotlib.pyplot
#import matplotlib as plt
import matplotlib.pyplot as plt


# lets try argparse since optparse has been deprecated
#from optparse import OptionParser
from argparse import ArgumentParser

#import astropy,
#from astropy.io import ascii

starttime=time.time()

default_infile='snc3_cdfs.input'

# First attempt at using ArgumentParser instead of OptionParser
parser = ArgumentParser(
 description='Bandmerge DES final cut single band files')
parser.add_argument("-i", "--infile", dest="infile", 
                  default=default_infile, 
                  help="input file with datapath and FITS file list")
parser.add_argument("-o", "--outfile", dest="outfile", default='/tmp/tmp.fits', 
                  help="output filename including path")
parser.add_argument("-c", "--columns", dest="columns", 
                  default="all", 
                  help="comma separated list of output columns \
                  [not implemenetd]")
parser.add_argument("-p", "--plots", \
                  action="store_true", dest="plots", 
                  default=False, help="make a few plot a")

parser.add_argument("-v", "--version", action="store_true", dest="version", 
                  default="", help="print version number and  exit")

parser.add_argument("-verbose", "--verbose", \
                  action="store_true", dest="verbose", 
                  default=False, help="verbose option")
parser.add_argument("-q", "--quiet", \
                  action="store_true", dest="quiet", 
                  default=False, help="quiet option")

args = parser.parse_args()
infile=args.infile
outfile=args.outfile
columns=args.columns
plots=args.plots
verbose=args.verbose
if args.version:
    print VERSION
    sys.exit(0)

print 'outfile: ', outfile
print 'Reading input file: ', infile
# use atpy
tab=atpy.Table(infile,type='ascii',Reader=asciitable.NoHeader,delimiter=' ')    

# use native asciitable          
#asciitable.read(infile, Reader=asciitable.NoHeader)
  
# use ascitable to read table into numpy record array
#help(table)
nfiles=len(tab.col1) -1
print 'Number of file to process: ', nfiles
print 'shape: ', tab.shape
#print 'dtype: ', tab.dtype
for row_vals in tab:  # iterate over table rows
  print row_vals  # print list of vals in each row
  
filters=[_[:-1] for _  in  tab.col1[1:]] #remove the last character 
files= tab.col2[1:]
inpath=tab.col2[0]

print "Elapsed time %.3f seconds" % (time.time() - starttime)

# read in all the FITS files

hdulists= [pyfits.open(inpath+x) for x in files] 

# dump out the header info 
quiet=False
if not (quiet):
  ifile=-1
  for hdulist in hdulists:  # iterate over the hdu
    ifile=ifile+1
    print 'Number of extensions: ',len(hdulists[ifile])
    print hdulists[ifile].info()
    columns=hdulists[ifile][2].columns
    print columns.info

# Read extension 2
ext=2
tables= [pyfits.getdata(inpath+x,ext) for x in files] 

if (plots):
  ifile=0
  for table in tables:  # iterate over the hdu
    ifile=ifile+1

    classifier=table['CLASS_STAR']

    stars = (classifier > 0.85)
    notstars = (classifier <0.85)

    xdata=table['alphawin_j2000']
    ydata=table['deltawin_j2000']

    plt.figure(num=None, figsize=(10, 10))
    plt.title(files[ifile-1])
    plt.xlabel('RA')
    plt.ylabel('Declination')

    label='non-stellar: ' + str(len(xdata[notstars]))
    plt.plot(xdata[notstars], ydata[notstars], 'r+', ms=1, c='r', 
     label=label)

    label='stellar: ' + str(len(xdata[stars]))
    plt.plot(xdata[stars], ydata[stars], 'b+', ms=2, c='b', 
     label=label)

    plt.legend(loc=2)

    #plt.plot(xdata, ydata, 'r.', color='red', markersize=1)

    #plt.scatter(xdata,ydata, marker='.', color='r', s=4, linewidths=0)
    #plotid(right=True)

    plt.savefig('radec_file'+ str(ifile) + '.png')
   
if (plots): exit("Exiting after plots")

print "Elapsed time %.3f seconds" % (time.time() - starttime)

spec_columns= ['ZZZnumber', 'ZZZALPHAWIN_J2000','ZZZDELTAWIN_J2000']
spec_columns = [str.lower(x) for x in spec_columns]

select_columns= ['Number']

itab=-1
for table in tables:  # iterate over table rows
  itab=itab+1
  print 'Input file, waveband, columns, rows: ', itab+1, \
   filters[itab], \
   len(tables[itab].columns), len(tables[itab])

coldefs=[]

# create list of new column names prepended with waveband
for i,(f,t) in enumerate(zip(filters,tables)):
	for c in t.columns:
		if str.lower(c.name) not in spec_columns:
			c1=copy.copy(c)
			c1.name=f+c1.name
			coldefs.append(c1)
		elif i==0:
			coldefs.append(c)
print "Elapsed time %.3f seconds" % (time.time() - starttime)
			
xtab=pyfits.new_table(coldefs,nrows=tables[0].shape[0])			

for i,(f,t) in enumerate(zip(filters,tables)):
	for c in t.columns:
		if str.lower(c.name) not in spec_columns:
			c1=copy.copy(c)
			c1.name=f+c1.name
			xtab.data[c1.name][:]=t[c.name]
		elif i==0:
			coldefs.append(c)
			xtab.data[c.name][:]=t[c.name]

#xtab.setval(test, 'test')
#xtab.add_datasum
#xtab.add_checksum

#help(xtab)
print 'Number of output rows: ', len(xtab.data)
print 'Output columns: ', len(xtab.columns)

print "Elapsed time %.3f seconds" % (time.time() - starttime)

xtab.writeto(outfile,clobber=True, checksum=True)

print "Elapsed time %.3f seconds" % (time.time() - starttime)
