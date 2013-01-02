
import time

import atpy
import asciitable

#import astropy
#from astropy.io import ascii

starttime=time.time()

verbose=0
infile='snc3_cdfs.input'

tab=atpy.Table('snc3_cdfs.input',type='ascii',Reader=asciitable.NoHeader,delimiter=' ')  
              
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
tables = [atpy.Table(inpath+x,hdu=2) for x in files] 

print "Elapsed time %.3f seconds" % (time.time() - starttime)

spec_columns= ['number', 'ALPHAWIN_J2000','DELTAWIN_J2000']
spec_columns = [str.lower(x) for x in spec_columns]

print 'Number or rows: ', len(tables[0])

# rename all columns in all bands except 
for f,t in zip(filters,tables):
        print "Elapsed time %.3f seconds" % (time.time() - starttime)
	for c in t.columns:
		if str.lower(c) not in spec_columns:
			t.rename_column(c,f+c)

print "Elapsed time %.3f seconds" % (time.time() - starttime)

# adds columns one by one
for t in tables[1:]:
        print "Elapsed time %.3f seconds" % (time.time() - starttime)
	for c in t.columns:
		print c
		if str.lower(c) not in spec_columns:
			tables[0].add_column(c,t[c])		
#if verbose: data1.describe()

print "Elapsed time %.3f seconds" % (time.time() - starttime)

tables[0].write('xx.fits')
# now write the fits output file

print "Elapsed time %.3f seconds" % (time.time() - starttime)
