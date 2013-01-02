def rd_rzfile(infile, fitsfile=None, debug=False):
  """
  read OzDES runs output rz format file and returns data as
  a pyfits object thing.
  includes option to write a FITs file

  useage:

  table=rd_rzfile(infile)

  rd_rzfile(infile, fitsfile='table.fits'

  todo; could specify a list of columns to return in Dictionary or Numpy record 
  array

  #Fib     Object                        RA   (2000)   dec      Rmag neb neg   
  #ze    ze_err  qe temp xcor   zx     zx_err qx   z_fin  zf_err  qa qop 
  #f fld  date ccd pl x_posn  y_posn  S/N   spmag  vsp   rsp   
  #RA(deg)   dec(deg)   comments

  #  2 DES_LRG_231                       2 27 36.17  -04 35 25.6 21.56  1  4  
  #0.18426 0.00001  3  2   2.95  0.17354 0.00065 2  0.17354 0.00065  0  1  
  #1 000 121216 4  0    4294  105147  1.09  20.35 21.66 21.71  
  #36.90071  -4.59044       

  version 0.1:
  brute force conversion; next version could be smarter maybe. The main 
  problem is that the RA, Dec is stored as 6 columns but the header has
  this as RA (2000) Dec so this would need some special processing. 

  """

  __version__ = '0.1'

  import pyfits
  import numpy as np

  import atpy
  import asciitable
  import astropy
  from astropy.io import ascii

  f = open(infile, 'r')

  data = f.readlines()
  print 'Number of rows in rz file: ', len(data)

  f = open(infile, 'r')
  iline=-1
  
  # read into a Python list: default is that list entries are type str
  # this is quite clumsy and does not parse the header line
  # all data should be stored as a list of strings. This ensures -00 is
  # parsed properly
  # the ra, dec have to explicitly converted to floats otherwise, pyfits
  # does something odd
  for line in f:
    iline=iline+1
    #print iline
    #print repr(line)
    # strip off the line feed
    line = line.strip()
    if iline == 0: print line
    columns = line.split()
    print 'Line, Number of columns: ', iline, len(columns)
    if iline == 0:
      if columns[0] == '#' or columns[0] == '#Fib': 
        print 'skipping comment line starting with: ', columns[0] 
        iline=iline-1
        print 'iline: ', iline
        continue

      fib=[columns[0]]
      if type(fib[iline]) != type('str'): print iline,' fib is not a string'
      object=[columns[1]]
      rahr=[columns[2]]
      ramin=[columns[3]]
      rasec=[columns[4]]
    
      ra_str = [rahr[0] + ' ' + ramin[0] + ' ' + rasec[0]]

      decdeg=[columns[5]]

      if type(decdeg[iline]) != type('str'): print iline, ' decdeg is not a string'
      decmin=[columns[6]]
      decsec=[columns[7]]

      dec_str = [decdeg[0] + ' ' + decmin[0] + ' ' + decsec[0]]

      if debug: print ra_str,' ',dec_str

      rmag=[columns[8]]
      neb=[columns[9]]
      neg=[columns[10]]
      ze=[columns[11]]
      ze_err=[columns[12]]
      qe=[columns[13]]
      temp=[columns[14]]
      xcor=[columns[15]]
      zx=[columns[16]]
      zx_err=[columns[17]]
      qx=[columns[18]]
      z_fin=[columns[19]]
      zf_err=[columns[20]]
      qa=[columns[21]]
      qop=[columns[22]]
      f=[columns[23]]
      fld=[columns[24]]
      date=[columns[25]]
      ccd=[columns[26]]
      pl=[columns[27]] 
      x_posn=[columns[28]]
      y_posn=[columns[29]]
      s_n=[columns[30]]
      spmag=[columns[31]]
      vsp=[columns[32]]   
      rsp=[columns[33]]   
      ra=[float(columns[34])]
      dec=[float(columns[35])]
      if len(columns) == 37:comment=[columns[36]]
      if len(columns) == 36:comment=[None]

    if iline > 0:
      if debug: print iline,' appending to list'

      fib.append(columns[0])
      if type(fib[iline]) != type('str'): print iline, ' fib is not a string'
 
      object.append(columns[1])
      if type(object[iline]) != type('str'): print iline, ' object is not a string'
      rahr.append(columns[2])
      if type(rahr[iline]) != type('str'): print iline, ' rahr is not a string'

      ramin.append(columns[3])
      if type(ramin[iline]) != type('str'): print iline, ' ramin is not a string'
      rasec.append(columns[4])
      if type(rahr[iline]) != type('str'): print iline, ' rasec is not a string'

      decdeg.append(columns[5])
      if type(decdeg[iline]) != type('str'): print iline, ' decdeg is not a string'
      decmin.append(columns[6])
      if type(decdeg[iline]) != type('str'): print iline, ' decdeg is not a string'
      decsec.append(columns[7])
      if type(decdeg[iline]) != type('str'): print iline, ' decdeg is not a string'
      ra_str.append(rahr[iline] + ' ' + ramin[iline] + ' ' + rasec[iline])
      dec_str.append(decdeg[iline] + ' ' + decmin[iline] + ' ' + decsec[iline])
      if debug: print ra_str[iline],' ',dec_str[iline]

      rmag.append(columns[8])
      neb.append(columns[9])
      neg.append(columns[10])
      ze.append(columns[11])
      ze_err.append(columns[12])
      qe.append(columns[13])
      temp.append(columns[14])
      xcor.append(columns[15])
      zx.append(columns[16])
      zx_err.append(columns[17])
      qx.append(columns[18])
      z_fin.append(columns[19])
      zf_err.append(columns[20])
      qa.append(columns[21])
      qop.append(columns[22])
      f.append(columns[23])
      fld.append(columns[24])
      date.append(columns[25])
      ccd.append(columns[26])
      pl.append(columns[27]) 
      x_posn.append(columns[28])
      y_posn.append(columns[29])
      s_n.append(columns[30])
      spmag.append(columns[31])
      vsp.append(columns[32])   
      rsp.append(columns[33])   
      ra.append(float(columns[34]))
      dec.append(float(columns[35]))
      if len(columns) == 37: comment.append(columns[36])
      if len(columns) == 36: comment.append('None')

  print iline, fib[iline], object[iline], rmag[iline], \
   ra[iline], dec[iline], comment[iline]

  print 'x_posn: ', x_posn
  print 'y_posn: ', y_posn

  print 'ra: ', ra
  print 'dec: ', dec

  #Fib     Object                        RA   (2000)   dec      Rmag  neb 
  #2 DES_LRG_231                       2 27 36.17  -04 35 25.6 21.56  1  
  col1=pyfits.Column(name='fib', format='J', array=fib)
  col2=pyfits.Column(name='object', format='32A', array=object)
  col3_5=pyfits.Column(name='ra_str', format='32A', array=ra_str)
  col6_8=pyfits.Column(name='dec_str', format='32A', array=dec_str)
  col9=pyfits.Column(name='rmag', format='E', array=rmag)
  col10=pyfits.Column(name='neb', format='J', array=neb)

  #neg   ze    ze_err  qe temp xcor   zx     zx_err qx   z_fin  
  #4 0.18426 0.00001  3  2   2.95  0.17354 0.00065 2  0.17354 
  col11=pyfits.Column(name='neg', format='J', array=neg)
  col12=pyfits.Column(name='ze', format='E', array=ze)
  col13=pyfits.Column(name='ze_err', format='E', array=ze_err)
  col14=pyfits.Column(name='qe', format='J', array=qe)
  col15=pyfits.Column(name='temp', format='J', array=temp)
  col16=pyfits.Column(name='xcor', format='E', array=xcor)
  col17=pyfits.Column(name='zx', format='E', array=zx)
  col18=pyfits.Column(name='zx_err', format='E', array=zx_err)
  col19=pyfits.Column(name='qx', format='J', array=qx)
  col20=pyfits.Column(name='z_fin', format='E', array=z_fin)

  #zf_err  qa qop f fld  date ccd pl x_posn  y_posn  
  #0.00065  0  1  1 000 121216 4  0    4294  105147  
  col21=pyfits.Column(name='zf_err', format='E', array=zf_err)
  col22=pyfits.Column(name='qa', format='32A', array=qa)
  col23=pyfits.Column(name='qop', format='J', array=qop)
  col24=pyfits.Column(name='f', format='J', array=f)
  col25=pyfits.Column(name='fld', format='J', array=fld)
  col26=pyfits.Column(name='date', format='J', array=date)
  col27=pyfits.Column(name='ccd', format='J', array=ccd)
  col28=pyfits.Column(name='pl', format='J', array=pl)
  col29=pyfits.Column(name='x_posn', format='J', array=x_posn)
  col30=pyfits.Column(name='y_posn', format='J', array=y_posn)

  #S/N   spmag  vsp   rsp   RA(deg)  dec(deg)   comments
  #1.09  20.35 21.66 21.71  36.90071  -4.59044       
  col31=pyfits.Column(name='s_n', format='E', array=s_n)
  col32=pyfits.Column(name='spmag', format='E', array=spmag)
  col33=pyfits.Column(name='vsp', format='E', array=vsp)
  col34=pyfits.Column(name='rsp', format='E', array=rsp)
  col35=pyfits.Column(name='ra', format='D', array=ra)
  col36=pyfits.Column(name='dec', format='D', array=dec)
  col37=pyfits.Column(name='comment', format='32A', array=comment)

  cols=pyfits.ColDefs([col1, col2, col3_5, col6_8, col9, col10,
   col11, col12, col13, col14, col15, col16, col17, col18, col19, col20,
   col21, col22, col23, col24, col25, col26, col27, col28, col29, col30,
   col31, col32, col33, col34, col35, col36, col37]) 
  
  table=pyfits.new_table(cols)
  tbhdu.writeto(fitsfile, clobber=True)

  print 'Number of data rows: ', len(fib), len(comment)

  return table

#f = open(infile, 'r')
#
#data = np.genfromtxt(f, dtype=('S2', 'f4', 'f4', 'f4'), names = True, \
#     skip_footer = 1, missing_values = ('nn'), filling_values=(np.nan))

if __name__ == '__main__':

  import table_stats

  inpath='/data/des/OzDES/'
  filename='X3_121216z.rz'
  filename='X3_121216z.rz.qso'
  infile = inpath + filename
  
  fitsfile='X3_121216z_qso' + '.fits'
  rd_rzfile(infile, fitsfile=fitsfile)

  infile=fitsfile
  table_stats.table_stats(infile, ext=1, verbose=True, debug=False)



