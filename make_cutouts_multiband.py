__version__="v0.0.1"  # 
"""

 DES cutout demo

 option to plot the weightmaps 
 to overplot the catalogue for an image.

 cutout needs to be padded so that size is correct and the centre is
 the centre requested. Maybe region file in the header.

 also maybe place some lookup table informatio scaling info into header for ds9 

 also need to cache the fits image so that it is not read multiple times
 pyfits might be doing the caching on the fly.

 create pngs and a webpage. 
 A table and a page per source
 webpage with free text input box and some tick boxes 

 see also fitsimage.py for making a jpeg
 https://code.google.com/p/wcs2kml/
 https://wcs2kml.googlecode.com/svn-history/r25/trunk/python/fitsimage.py  


"""

def make_cutouts_multiband(bands='r', detband='detr', 
  imagefiles=None, 
  listfile=None, format='region', width_arcsecs=10.0, 
  catfiles=None):

  """


  """

  import os, sys
  import time

  import pyfits
  import pyregion
  import cutout

  #import fits2png

  import matplotlib.pyplot as plt
  #if not interactive: matplotlib.use('Agg')

  import aplpy

  import plotid

  t0=time.time()

  base=os.path.basename(listfile)
  id=os.path.splitext(base)[0]

  weightmap = False


  # open ds9 region 
  if format == 'region':
    region = pyregion.open(listfile)

    irow=-1
    # print out the cordinates in degrees
    for rows in region:  # iterate over table rows
      irow=irow+1
      print irow+1, region[irow].coord_list[0], region[irow].coord_list[1]
  
    nrows=len(region)

  if format == 'ozdes':
    table= pyfits.getdata(listfile,1)
    ralist = table['RA']
    declist = table['Dec']
    object = table['object']
    comment = table['comment']
    redshift = table['z_fin']
    print 'ralist range: ', min(ralist), max(ralist)
    print 'declist range: ', min(declist), max(declist)
    nrows=len(ralist)

  # Read extension 2 of the catalog file
  ext=2
  catalog = pyfits.getdata(catalog_path+catalog_filename,ext)
  ra_catalog = catalog['alphawin_j2000']
  dec_catalog = catalog['deltawin_j2000']

  title=imagefiles 
  #plt.text(.5, .95, title, horizontalalignment='center') 

  # leave some space to add annotation at the top of the page
  plt.rc('figure.subplot', left=0.05, right=0.95, bottom=0.05, top=0.95, 
   wspace=0.0, hspace=0.0)

  fig=plt.figure(figsize=(12.0, 10.0))

  fig.text(0.1, 0.97, title, horizontalalignment='left', 
   color='blue', transform = plt.gcf().transFigure) 

  plt.xticks=[]
  plt.yticks=[]
  label=os.path.basename(__file__)
  plotid.plotid(label=label)

  nxplots=5
  nyplots=6

  irow=-1
  iplot=0
  

  #print plt.get_gca()
  #print plt.get_gcf()
  isource=0
  ifig=1
  #for rows in region:  # iterate over table rows

  for rows in ralist:  # iterate over table rows
    print 'Elpased time: %.2f seconds' %(time.time() - t0)
    irow=irow+1
    isource=isource+1
    print irow, ' of ', nrows
    #if irow > nxplots*nyplots: break

    if format == 'region':
      ra=region[irow].coord_list[0]
      dec=region[irow].coord_list[1]

    if format == 'ozdes':
      ra=ralist[irow]
      dec=declist[irow]

    iband=-1
    for band in bands:  # iterate over the bands  
      iband=iband+1
      iplot=iplot+1
      outfile='cutout' + str(irow+1) + band + '.fits'
      outfile=None
      verbose=True
      xc=ra
      yc=dec
      imagefile=imagefiles[iband]
      print 'input image: ', imagefile

      # width in arcsecs
      width_arcsecs=10.0
      # convert to semi-width in degrees
      xw=(0.5*width_arcsecs)/3600.0 
      yw=(0.5*width_arcsecs)/3600.0 
    
      # create cutout FITS file
      imagefile=imagefiles[iband]
      image=cutout.cutout(imagefile, xc, yc, xw=xw, yw=yw, units='wcs', 
       outfile=outfile, clobber=True, 
       useMontage=False, coordsys='celestial', verbose=verbose)
      image = image.data

      ax=fig.add_subplot(nxplots,nyplots,iplot,
       frameon=True, xticks=[], yticks=[])
      ax.imshow(image)

      if iband == 0: ax.text(0.1, 0.80, str(isource), 
       transform=plt.gca().transAxes)

      ax.text(0.9, 0.80, band, transform=plt.gca().transAxes)

      if format == 'ozdes':
        annotation=object[isource-1].strip()
        if iband == 0: ax.text(0.1, 0.02, annotation, 
          verticalalignment='baseline',
          transform=plt.gca().transAxes)

        annotation=comment[isource-1].strip()
        if iband == 0: ax.text(0.1, 0.1, annotation, 
          transform=plt.gca().transAxes)

        annotation=str(redshift[isource-1]).strip()
        if iband == 0: ax.text(0.5, 0.1, annotation, 
          transform=plt.gca().transAxes)


      if iplot == nxplots*nyplots:
        print 'nxplots, nyplots, iplot, isource: ', \
         nxplots, nyplots, iplot, isource
        iplot=0
        strfigno= '%4.4d' % (ifig)
        #plt.savefig(id+'_cutouts_multiband_' + str(ifig) + '.png', dpi=150)
        #plt.savefig(id+'_cutouts_multiband_' + strfigno + '.png', dpi=150)
        plt.savefig(id+'_cutouts_multiband_' + strfigno + '.png', dpi=100)

        if ifig == 1: plt.show()
        ifig=ifig+1
        fig=plt.figure(ifig,figsize=(12.0, 10.0))
        plotid.plotid(label=label)

  print 'nxplots, nyplots, iplot, isource: ', \
         nxplots, nyplots, iplot, isource
  iplot=0
  strfigno= '%4.4d' % (ifig)
  #plt.savefig(id+'_cutouts_multiband_' + str(ifig) + '.png', dpi=150)
  #plt.savefig(id+'_cutouts_multiband_' + strfigno + '.png', dpi=150)
  plt.savefig(id+'_cutouts_multiband_' + strfigno + '.png', dpi=100)


if __name__ == '__main__':

  from argparse import ArgumentParser

  default_band='r'
  default_detband='detr'

  # First attempt at using ArgumentParser instead of OptionParser
  parser = ArgumentParser(
    description='Create a montage of DES cutouts for a single field')

  parser.add_argument("-b", "--bands", dest="bands", 
                  default=default_band, 
                  help="input band names [u,g,r,i,z,Y]")
  parser.add_argument("-d", "--detband", dest="detband", 
                  default=default_detband, 
                  help="input Sextractor detection band [u,g,r,i,z,Y]")
  parser.add_argument("-v", "--version", action="store_true", dest="version", 
                  default="", help="print version number and  exit")

  args = parser.parse_args()
  if args.version:
    print __version__
    sys.exit(0)

  bands=args.bands
  detband=args.detband

  bands=['u','g','r','i','z','Y']
  nbands=len(bands)
  imagefiles=['','','','','','','']
  iband=-1

  # iterate over the bands making arrays with all the filenames 
  for band in bands:  
    iband=iband+1
    image_path='/data/des/SV/snx3_vvds02hr/v2/' + band + '/'
    image_filename="vvds02hr_" + band + ".fits"
    imagefile= image_path + image_filename
    imagefiles[iband]=imagefile

    weightmap_filename = 'vvds02hr_weight_Y.fits'
    weightfile = image_path + weightmap_filename

    catalog_path = image_path
    catalog_filename="vvds02hr_" + band + "_" + detband + "_cat.fits"


  list_path='./'
  list_filename = "snx3_dr9qso.reg"
  list_filename = "snx3_vvdsqso.reg"
  format='region'

  list_path='/data/des/OzDES/'
  list_filename='X3_121216z_qso.fits'
  format='ozdes'

  listfile = list_path + list_filename

  print 'listfile: ', listfile
  make_cutouts_multiband(bands=bands, detband=detband, 
   listfile=listfile, format=format, 
   imagefiles=imagefiles)
