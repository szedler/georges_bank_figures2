#! /usr/bin/env python 

import numpy as np 
import matplotlib.pyplot as plt 
import netCDF4
import cartopy.crs as ccrs
import cartopy.feature as cfea
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

vmx=1*10**-5

# load divergence 
f=np.load('divergence_UV_delU.npz')
delUdata=f['delUdata'][:]
delUmask=f['delUmask'][:]
lon=f['lon'][:]
lat=f['lat'][:]
H=f['H'][:]
f.close()
delU=np.ma.masked_array(delUdata,mask=delUmask)

# reduce size of Ssea to GB region 
lonGB=lon[:,80:]
latGB=lat[:,80:]
delU=delU[:,:,80:]

levels0=np.arange(0,350,50)
levels1=np.arange(500,5010,500)
levs=np.hstack([levels0,levels1])

# assign box numbers for low resolution grid (33 low/high bounds in x and y direction) 
# open low and high bounds for X and Y grid (boxes)
f=np.load('mask_GB_lores.npz')
Xlo=f['Xlo'][:]
Ylo=f['Ylo'][:]
Xhi=f['Xhi'][:]
Yhi=f['Yhi'][:]
B0=f['B0'][:]
f.close()

XC=(Xlo+Xhi)/2
YC=(Ylo+Yhi)/2

f=np.load('UV_vectors_surface.npz')
lonSS=f['lonSS'][:]
latSS=f['latSS'][:]
UseaSS=f['USS'][:]
VseaSS=f['VSS'][:]
f.close()

# Speed
SS=np.sqrt(UseaSS**2+VseaSS**2)

US=np.ma.masked_where(np.abs(SS)>10,UseaSS)
VS=np.ma.masked_where(np.abs(SS)>10,VseaSS)

fig=plt.figure(figsize=(10,8)) 
ax1=fig.add_subplot(221,projection=ccrs.PlateCarree())
ax1.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
ax1.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img10=ax1.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='k',transform=ccrs.PlateCarree())
ax1.add_feature(cfea.COASTLINE,edgecolor='white')
gl=ax1.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
ax1.set_title('Winter')
ax1.text(-70,42.8,'(a)')
ax1.clabel(img10,levels=levs,fontsize=12,colors="k")
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
img1=ax1.pcolormesh(lonGB,latGB,delU[0,:,:],cmap='bwr',vmin=-1*vmx,vmax=vmx)
q1=ax1.quiver(lonSS,latSS,US[0,:,:],VS[0,:,:],scale=1,scale_units='inches',color='k',linewidths=1.5,edgecolor='k')
ax1.quiverkey(q1,X=0.1,Y=-0.1,U=0.45,label='length = 0.45 m/s',labelpos='E',color='k')
ax2=fig.add_subplot(222,projection=ccrs.PlateCarree())
ax2.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
ax2.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img11=ax2.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='k',transform=ccrs.PlateCarree())
img2=ax2.pcolormesh(lonGB,latGB,delU[1,:,:],cmap='bwr',vmin=-1*vmx,vmax=vmx)
q2=ax2.quiver(lonSS,latSS,US[1,:,:],VS[1,:,:],scale=1,scale_units='inches',color='k',edgecolor='k',linewidths=1.5)
ax2.clabel(img11,levels=levs,fontsize=12,colors='k')
ax2.grid()
ax2.set_xlim(np.min(XC)-0.5,np.max(XC)+0.5)
ax2.set_ylim(np.min(YC)-0.5,np.max(YC)+0.5)
ax2.add_feature(cfea.COASTLINE,edgecolor='white')
ax2.text(-70,42.8,'(b)')
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
img10=ax3.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='k',transform=ccrs.PlateCarree())
ax3.add_feature(cfea.COASTLINE,edgecolor='white')
gl=ax3.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
ax3.set_title('Summer')
img3=ax3.pcolormesh(lonGB,latGB,delU[2,:,:],cmap='bwr',vmin=-1*vmx,vmax=vmx)
q3=ax3.quiver(lonSS,latSS,US[2,:,:],VS[2,:,:],scale=1,scale_units='inches',color='k',edgecolor='k',linewidths=1.5)
ax3.clabel(img10,levels=levs,fontsize=12,colors='k')
ax3.grid()
ax3.set_xlim(np.min(XC)-0.5,np.max(XC)+0.5)
ax3.set_ylim(np.min(YC)-0.5,np.max(YC)+0.5)
ax3.text(-70,42.8,'(c)')
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
img2=ax4.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='k',transform=ccrs.PlateCarree())
ax4.add_feature(cfea.COASTLINE,edgecolor='white')
ax4.set_title('Fall')
ax4.text(-70,42.8,'(d)')
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
img4=ax4.pcolormesh(lonGB,latGB,delU[3,:,:],cmap='bwr',vmin=-1*vmx,vmax=vmx)
q4=ax4.quiver(lonSS,latSS,US[3,:,:],VS[3,:,:],scale=1,scale_units='inches',color='k',edgecolor='k',linewidths=1.5)
ax4.clabel(img2,levels=levs,fontsize=12,colors='k')
ax4.grid()
ax4.set_xlim(np.min(XC)-0.5,np.max(XC)+0.5)
ax4.set_ylim(np.min(YC)-0.5,np.max(YC)+0.5)

ax5=fig.add_axes([0.17,0.06,0.7,0.02])
plt.colorbar(img1,cax=ax5,orientation="horizontal")
plt.xlabel('Divergence: '+r'$\frac{\partial U}{\partial x}+\frac{\partial V}{\partial y}$'+' (rad/s)')
fig.savefig('figure4.png')

