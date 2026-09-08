#! /usr/bin/env python 

import numpy as np 
import matplotlib.pyplot as plt 
import netCDF4
import cartopy.crs as ccrs
import cartopy.feature as cfea
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

f=np.load('delta_RHO.npz')
DRHOdata=f['DRHOBdata'][:]
DRHOmask=f['DRHOBmask'][:]
f.close()
DRHO=np.ma.masked_array(DRHOdata,mask=DRHOmask)

f=np.load('UV_surface.npz')
lonSS=f['lonSS'][:]
latSS=f['latSS'][:]
UseaSSdata=f['UseaSSdata'][:]
UseaSSmask=f['UseaSSmask'][:]
VseaSSdata=f['VseaSSdata'][:]
VseaSSmask=f['VseaSSmask'][:]
f.close()

UseaSS=np.ma.masked_array(UseaSSdata,mask=UseaSSmask)
VseaSS=np.ma.masked_array(VseaSSdata,mask=VseaSSmask)

f=np.load('XY.npz')
XC=f['XC'][:]
YC=f['YC'][:]
f.close()

nc=netCDF4.Dataset('mabgom4_hycom.nc')
lon=nc.variables['lon_rho'][:]
lat=nc.variables['lat_rho'][:]
H=nc.variables['h'][:]
nc.close()
lonGB=lon[:,80:] 
latGB=lat[:,80:]

levels0=np.arange(0,350,50)
levels1=np.arange(500,5010,500)
levs=np.hstack([levels0,levels1])

# make plot of box numbers 
fig=plt.figure(figsize=(10,8)) 
ax1=fig.add_subplot(221,projection=ccrs.PlateCarree())
ax1.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
ax1.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img10=ax1.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='w',transform=ccrs.PlateCarree())
ax1.add_feature(cfea.COASTLINE,edgecolor='white')
gl=ax1.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
ax1.set_title('Winter')
ax1.clabel(img10,levels=levs,fontsize=12,colors="w")
ax1.grid()
ax1.set_xlim(np.min(XC)-0.5,np.max(XC)+0.5)
ax1.set_ylim(np.min(YC)-0.5,np.max(YC)+0.5)
gl.top_labels=False
gl.bottom_labels=False
gl.left_labels=True
gl.right_labels=False
gl.xlines=True
gl.xlocator=mticker.FixedLocator([-70,-69,-68,-67,-66,-65])
gl.ylocator=mticker.FixedLocator([39,39.5,40,40.5,41,41.5,42,42.5])
gl.xformatter= LONGITUDE_FORMATTER
gl.yformatter=LATITUDE_FORMATTER
gl.xlabel_style={'color':'black','weight':'normal'}
gl.ylabel_style={'color':'black','weight':'normal'}
cmap=plt.cm.viridis
cmap.set_bad("mediumpurple")
img1=ax1.pcolormesh(lonGB,latGB,np.abs(DRHO[0,:,:]),cmap=cmap,vmin=0,vmax=26.6)
q1=ax1.quiver(lonSS,latSS,UseaSS[0,:,:],VseaSS[0,:,:],scale=1,scale_units='inches',color='w',linewidths=1.5,edgecolor='w')

ax2=fig.add_subplot(222,projection=ccrs.PlateCarree())
ax2.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
ax2.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img11=ax2.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='w',transform=ccrs.PlateCarree())
img2=ax2.pcolormesh(lonGB,latGB,np.abs(DRHO[1,:,:]),cmap=cmap,vmin=0,vmax=26.6)
q2=ax2.quiver(lonSS,latSS,UseaSS[1,:,:],VseaSS[1,:,:],scale=1,scale_units='inches',color='w',edgecolor='w',linewidths=1.5)
ax2.clabel(img11,levels=levs,fontsize=12,colors='w')
ax2.grid()
ax2.set_xlim(np.min(XC)-0.5,np.max(XC)+0.5)
ax2.set_ylim(np.min(YC)-0.5,np.max(YC)+0.5)
ax2.add_feature(cfea.COASTLINE,edgecolor='white')
gl=ax2.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
ax2.set_title('Spring')
gl.top_labels=False
gl.bottom_labels=False
gl.left_labels=False
gl.right_labels=False
gl.xlines=True
gl.xlocator=mticker.FixedLocator([-70,-69,-68,-67,-66,-65])
gl.ylocator=mticker.FixedLocator([39,39.5,40,40.5,41,41.5,42,42.5])
gl.xformatter= LONGITUDE_FORMATTER
gl.yformatter=LATITUDE_FORMATTER
gl.xlabel_style={'color':'black','weight':'normal'}
gl.ylabel_style={'color':'black','weight':'normal'}

ax3=fig.add_subplot(223,projection=ccrs.PlateCarree())
ax3.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
ax3.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img10=ax3.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='w',transform=ccrs.PlateCarree())
ax3.add_feature(cfea.COASTLINE,edgecolor='white')
gl=ax3.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
ax3.set_title('Summer')
img3=ax3.pcolormesh(lonGB,latGB,np.abs(DRHO[2,:,:]),cmap=cmap,vmin=0,vmax=26.6)
q3=ax3.quiver(lonSS,latSS,UseaSS[2,:,:],VseaSS[2,:,:],scale=1,scale_units='inches',color='w',edgecolor='w',linewidths=1.5)
ax3.quiverkey(q1,X=0.1,Y=-0.1,U=0.45,label='length = 0.45 m/s',labelpos='E',color='k',linewidths=2)
ax3.clabel(img10,levels=levs,fontsize=12,colors='w')
ax3.grid()
ax3.set_xlim(np.min(XC)-0.5,np.max(XC)+0.5)
ax3.set_ylim(np.min(YC)-0.5,np.max(YC)+0.5)
gl.top_labels=False
gl.right_labels=False
gl.left_ylabels=True
gl.bottom_labels=True
gl.xlines=True
gl.xlocator=mticker.FixedLocator([-70,-69,-68,-67,-66,-65])
gl.ylocator=mticker.FixedLocator([39,39.5,40,40.5,41,41.5,42,42.5])
gl.xformatter= LONGITUDE_FORMATTER
gl.yformatter=LATITUDE_FORMATTER
gl.xlabel_style={'color':'black','weight':'normal'}
gl.ylabel_style={'color':'black','weight':'normal'}

ax4=fig.add_subplot(224,projection=ccrs.PlateCarree())
ax4.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
ax4.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img4=ax4.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='w',transform=ccrs.PlateCarree())
ax4.add_feature(cfea.COASTLINE,edgecolor='white')
ax4.set_title('Fall')
gl=ax4.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
gl.top_labels=False
gl.right_labels=False
gl.left_labels=False
gl.bottom_labels=True
gl.xlines=True
gl.xlocator=mticker.FixedLocator([-70,-69,-68,-67,-66,-65])
gl.ylocator=mticker.FixedLocator([39,39.5,40,40.5,41,41.5,42,42.5])
gl.xformatter= LONGITUDE_FORMATTER
gl.yformatter=LATITUDE_FORMATTER
gl.xlabel_style={'color':'black','weight':'normal'}
gl.ylabel_style={'color':'black','weight':'normal'}
img13=ax4.pcolormesh(lonGB,latGB,np.abs(DRHO[3,:,:]),cmap=cmap,vmin=0,vmax=26.6)
q4=ax4.quiver(lonSS,latSS,UseaSS[3,:,:],VseaSS[3,:,:],scale=1,scale_units='inches',color='w',edgecolor='w',linewidths=1.5)
ax4.clabel(img4,levels=levs,fontsize=12,colors='w')
ax4.grid()
ax4.set_xlim(np.min(XC)-0.5,np.max(XC)+0.5)
ax4.set_ylim(np.min(YC)-0.5,np.max(YC)+0.5)

ax1.text(-70, 42.75, '(a)')
ax2.text(-70, 42.75, '(b)')
ax3.text(-70, 42.75, '(c)')
ax4.text(-70, 42.75, '(d)')

ax5=fig.add_axes([0.17,0.06,0.7,0.02])
plt.colorbar(img13,cax=ax5,orientation="horizontal")
plt.xlabel('Density anomaly: bottom minus top (kg/m3)')

fig.savefig('figure_S2.png')
