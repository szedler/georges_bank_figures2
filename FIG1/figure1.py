#! /usr/bin/env python

def define_polygonD6(lonr,latr):
    import numpy as np
    from shapely.geometry.polygon import Polygon

    # we start with the 11 point mask polygonD5 
    
    #dd='/Users/sarahzedler/darwin/scripts/roms/vorticity/'
    f=np.load('polygonD5.npz') 
    
    X=f['IX']
    Y=f['IY']

    f.close()

    # remove next to last point 

    # we remove the next to last point     

    XD=np.zeros((10))
    YD=XD.copy()
    
    XD[:-2]=X[:-3]
    YD[:-2]=Y[:-3]

    XD[-2:]=X[-2:]
    YD[-2:]=Y[-2:]

    XD[-1]=X[-1]
    YD[-1]=Y[-1]
 
    LONR=np.zeros((10))
    LATR=LONR.copy()
    for ii in range(0,10):
        LONR[ii]=lonr[int(YD[ii]),int(XD[ii])]
        LATR[ii]=latr[int(YD[ii]),int(XD[ii])]

    polygon=Polygon([ (int(X[0]),int(Y[0])),(int(X[1]),int(Y[1])),(int(X[2]),int(Y[2])),(int(X[3]),int(Y[3])),(int(X[4]),int(Y[4])),(int(X[5]),int(Y[5])),(int(X[6]),int(Y[6])),(int(X[7]),int(Y[7])),(int(X[8]),int(Y[8])),(int(X[9]),int(Y[9]))])

    polygon2=Polygon([ (lonr[int(Y[0]),int(X[0])],latr[int(Y[0]),int(X[0])]),(lonr[int(Y[1]),int(X[1])],latr[int(Y[1]),int(X[1])]),(lonr[int(Y[2]),int(X[2])],latr[int(Y[2]),int(X[2])]),(lonr[int(Y[3]),int(X[3])],latr[int(Y[3]),int(X[3])]),(lonr[int(Y[4]),int(X[4])],latr[int(Y[4]),int(X[4])]),(lonr[int(Y[5]),int(X[5])],latr[int(Y[5]),int(X[5])]),(lonr[int(Y[6]),int(X[6])],latr[int(Y[6]),int(X[6])]),(lonr[int(Y[7]),int(X[7])],latr[int(Y[7]),int(X[7])]),(lonr[int(Y[8]),int(X[8])],latr[int(Y[8]),int(X[8])]),(lonr[int(Y[9]),int(X[9])],latr[int(Y[9]),int(X[9])])])

    return polygon,polygon2,LONR,LATR,XD,YD

import netCDF4
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Polygon
import cartopy.crs as ccrs
import cartopy.feature as cfea
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
#from subroutine_polygonD6 import define_polygonD6

levels0=np.arange(50,200,100)
levels1=np.arange(350,5500,1000)
levs=np.hstack([levels0,levels1])

f=np.load('ssh_2004_2006.npz')
ssh2004data=f['ssh2004data'][:]
ssh2004mask=f['ssh2004mask'][:]
ssh2006data=f['ssh2006data'][:]
ssh2006mask=f['ssh2006mask'][:]
lon=f['lon'][:]
lat=f['lat'][:]
f.close()

ssh2004=np.ma.masked_array(ssh2004data,mask=ssh2004mask)
ssh2006=np.ma.masked_array(ssh2006data,mask=ssh2006mask)

# define polygon representing Off-Slope Region (OSR)
polygon,polygon2,LONPD,LATPD,Xdummy,Ydummy=define_polygonD6(lon,lat)

# GET BATHYMETRY for our domain
nc=netCDF4.Dataset('/Users/sarahzedler/darwin/roms/mabgom4_hycom.nc')
HGB=np.squeeze(nc.variables['h'][:])
nc.close()

lonGB=np.ma.masked_where(np.logical_or(lon<=-74,np.logical_or(lon>=-64,np.logical_or(lat<=38,lat>=46))),lon)
latGB=np.ma.masked_where(lonGB.mask==True,lat)

# load surface deployed Lagrangian particle trajectories 

f=np.load('XY_2004_2006.npz')
XCALL2004=f['XCALL2004'][:]
YCALL2004=f['YCALL2004'][:]
XCALL2006=f['XCALL2006'][:]
YCALL2006=f['YCALL2006'][:]
f.close()

# 50 12.43 hour time steps is 
# approx 26 days... 
tlen2=50
tt=np.arange(0,8)*tlen2/8 
ttide=np.arange(0,50)
t0days=ttide[0]*12.43/24

tl=np.zeros((10,tlen2))
for pp in range(0,10):
    tl[pp,:]=np.arange(0,tlen2)*12.43/24

tti=np.arange(0,tlen2)
tda=tti*12.43/24
td=np.interp(tt,tti,tda)
tstr=np.floor((td+t0days)*10)/10
xtl=[str(tstr[0]),str(tstr[1]),str(tstr[2]),str(tstr[3]),str(tstr[4]),str(tstr[5]),str(tstr[6]),str(tstr[7])]

JET=mpl.colormaps['jet'].resampled(52)

fig3=plt.figure(figsize=(13,6))
ax1=fig3.add_subplot(121,projection=ccrs.PlateCarree())
ax1.set_extent([np.min(lonGB),np.max(lonGB),np.min(latGB),np.max(latGB)],crs=ccrs.PlateCarree())
ax1.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img3=ax1.pcolormesh(lon,lat,ssh2004,cmap='bwr',vmin=-0.8,vmax=0.8)
img2=ax1.contour(lonGB,latGB,HGB,levels=levs,linewidths=2,transform=ccrs.PlateCarree())
ax1.clabel(img2,levels=levs,fontsize=16)
ax1.add_feature(cfea.COASTLINE,edgecolor='white')
ax1.text(-76,46.5,'(a)')
gl=ax1.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
gl.top_labels=False
gl.right_labels=False
gl.left_labels=True
gl.bottom_labels=True
gl.xlines=True
gl.xlocator=mticker.FixedLocator([-80,-77,-74,-71,-68,-65])
gl.ylocator=mticker.FixedLocator([36,38,40,42,44,46])
gl.xformatter= LONGITUDE_FORMATTER
gl.yformatter=LATITUDE_FORMATTER
gl.xlabel_style={'color':'black','weight':'normal'}
gl.ylabel_style={'color':'black','weight':'normal'}

ax3=fig3.add_axes([0.2,0.1,0.6,0.03])
ax3.pcolormesh(tl,cmap='jet',vmin=0,vmax=np.max(tl))
ax3.set_xticks(np.arange(0,tlen2,tlen2/8))
ax3.set_xticklabels(xtl)
ax3.set_yticklabels('')
ax3.set_xlabel('Number of Days after Release (ref. September 1, given year)')
ax1.set_title('2004')
ax1.set_extent([-75,-63,38,46],crs=ccrs.PlateCarree())

ax4=fig3.add_subplot(122,projection=ccrs.PlateCarree())
ax4.set_extent([np.min(lonGB),np.max(lonGB),np.min(latGB),np.max(latGB)],crs=ccrs.PlateCarree())
ax4.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img3=ax4.pcolormesh(lon,lat,ssh2006,cmap='bwr',vmin=-0.8,vmax=0.8)
img2=ax4.contour(lonGB,latGB,HGB,levels=levs,linewidths=2,transform=ccrs.PlateCarree())
ax4.clabel(img2,levels=levs,fontsize=16)
ax4.add_feature(cfea.COASTLINE,edgecolor='white')
ax4.text(-76,46.5,'(b)')
gl=ax4.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
gl.top_labels=False
gl.right_labels=False
gl.left_labels=False
gl.bottom_labels=True
gl.xlines=True
gl.xlocator=mticker.FixedLocator([-80,-77,-74,-71,-68,-65])
gl.ylocator=mticker.FixedLocator([36,38,40,42,44,46])
gl.xformatter= LONGITUDE_FORMATTER
gl.yformatter=LATITUDE_FORMATTER
gl.xlabel_style={'color':'black','weight':'normal'}
gl.ylabel_style={'color':'black','weight':'normal'}

for it in range(0,50):
    for iflt in range(0,1000):
        ax1.plot(XCALL2004[it:it+2,iflt],YCALL2004[it:it+2,iflt],'-',color=JET(it),linewidth='0.75')
ax4.set_title('2006')
ax4.set_extent([-75,-63,38,46],crs=ccrs.PlateCarree())

for it in range(0,50):
    for iflt in range(0,1000):
        ax4.plot(XCALL2006[it:it+2,iflt],YCALL2006[it:it+2,iflt],'-',color=JET(it),linewidth='0.75')
ax2=fig3.add_axes([0.93,0.2,0.015,0.6])
plt.colorbar(img3,cax=ax2,orientation="vertical")
ax2.set_ylabel('SSHA on September 17 (m; in given year)')
lonGB2=np.ma.masked_where(np.logical_or(lon<=-74,np.logical_or(lon>=-63,np.logical_or(lat<=38,lat>=46))),lon)
latGB2=np.ma.masked_where(lonGB.mask==True,lat)
ax7=fig3.add_axes([0.125*0.78,0.47*1.02,0.18*1.2,0.3*0.9],projection=ccrs.PlateCarree())
ax7.set_extent([np.min(lonGB2),np.max(lonGB2),np.min(latGB2),np.max(latGB2)],crs=ccrs.PlateCarree())
ax7.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
ax7.add_feature(cfea.COASTLINE,edgecolor='white')
for ii in range(0,10):
    ax7.plot(LONPD[ii:ii+2],LATPD[ii:ii+2],'b',linewidth=2)
x1=LONPD[0]
y1=LATPD[0]
x2=LONPD[-1]
y2=LATPD[-1]
msp=(y2-y1)/(x2-x1)
xx=np.arange(x1,x2,(x2-x1)/50)
yy=msp*(xx-x1)+y1
ax7.plot(LONPD,LATPD,'bo',markeredgecolor='w',markersize=8)
ax7.plot(xx,yy,'b-')
ax7.set_extent([-75,-59.5,34,46],crs=ccrs.PlateCarree())
pg=Polygon([[LONPD[0],LATPD[0]],[LONPD[1],LATPD[1]],[LONPD[2],LATPD[2]],[LONPD[3],LATPD[3]],[LONPD[4],LATPD[4]],[LONPD[5],LATPD[5]],[LONPD[6],LATPD[6]],[LONPD[7],LATPD[7]],[LONPD[8],LATPD[8]],[LONPD[9],LATPD[9]]],closed=True,hatch="X",color='r',fill=True)
ax7.add_artist(pg)
img2=ax7.contour(lonGB2,latGB2,HGB,levels=levs,linewidths=2,transform=ccrs.PlateCarree())
ax7.text(-68.4,41.2,'GB',fontsize=10,color='r',fontweight='bold')
ax7.text(-68.8,42.7,'GOM',fontsize=10,color='r',fontweight='bold')
ax7.text(-67,39.3,'OSR',fontsize=10,color='w',fontweight='bold')
gl=ax7.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
gl.top_labels=True
gl.bottom_labels=False
gl.left_labels=False
gl.right_labels=True
gl.xlines=True
gl.xlocator=mticker.FixedLocator([-71,-65])
gl.ylocator=mticker.FixedLocator([36,40,44,48])
gl.xformatter= LONGITUDE_FORMATTER
gl.yformatter=LATITUDE_FORMATTER
gl.xlabel_style={'color':'black','weight':'normal'}
gl.ylabel_style={'color':'white','weight':'normal'}

fig3.savefig('figure1.png')

