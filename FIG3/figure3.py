#! /usr/bin/env python

import netCDF4
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cfea

# define boxes in center of domain (outline) 
Xbot=np.arange(-68.28,-67.28,0.01)
Ybot=np.ones(np.shape(Xbot))*41.1  

Ylft=np.arange(41.1,41.7,0.01)
Xlft=np.ones(np.shape(Ylft))*-68.28

Xtop0=np.arange(-68.28,-67.78,0.01)
Ytop0=np.ones(np.shape(Xtop0))*41.7

Ytop1=np.arange(41.7,42.0,0.01)
Xtop1=np.ones(np.shape(Ytop1))*-67.78

Xtop2=np.arange(-67.78,-67.28,0.01)
Ytop2=np.ones(np.shape(Xtop2))*42.0

Yrig=np.arange(41.1,42,0.01)
Xrig=np.ones(np.shape(Yrig))*-67.28

# END define boxes 

lly1=np.arange(40.2,42.4,0.3)
llx1=np.arange(-69.28,-65.7,0.5)

# make a FULL range box index
lxc=(llx1[1:]+llx1[:-1])/2
lyc=(lly1[1:]+lly1[:-1])/2
XC,YC=np.meshgrid(lxc,lyc)

# load up percent drifters by season that remain on bank, conditioned on the box of deployment
f=np.load('percent_drifters_remaining.npz')
PGBIdata=f['PGBIdata'][:]
PGBImask=f['PGBImask'][:]
f.close()

PGBI=np.ma.masked_array(PGBIdata,mask=PGBImask)

#dni='/Users/sarahzedler/darwin/scripts/github/'
nc=netCDF4.Dataset('mabgom4_hycom.nc')
lon=np.squeeze(nc.variables["lon_rho"][:])
lat=np.squeeze(nc.variables["lat_rho"][:])
H=nc.variables["h"][:]
nc.close()

# set contour levels for bottom bathymetry (meters) 
levels0=np.arange(0,350,50)
levels1=np.arange(500,5010,500)
levs=np.hstack([levels0,levels1])

f=np.load('percent_drifter_on_GB_100days_total.npz')
PNGB1Dmean=f['PNGB1Dmean'][:]
PNGB1Dstd=f['PNGB1Dstd'][:]
tdy=f['tdy'][:]
tPEFtxt=f['tPEFtxt'][:]
f.close()

fig = plt.figure(figsize=(12,6)) 
gs=gridspec.GridSpec(2,3,figure=fig)
axa=fig.add_subplot(gs[0,0],projection=ccrs.PlateCarree())
axa.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
axa.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img00=axa.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='black',transform=ccrs.PlateCarree())
axa.clabel(img00,levels=levs,fontsize=12)
axa.add_feature(cfea.COASTLINE,edgecolor='white')
gl=axa.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
axa.set_title('Winter',color='b')
img1=axa.pcolormesh(XC,YC,PGBI[0,:,:],cmap='jet',vmin=0,vmax=60)
gl.top_labels=False
gl.bottom_labels=False
gl.left_labels=True
gl.right_labels=False
gl.xlines=True
axa.text(-70.5,42.75,'(a)')
axa.plot(Xbot,Ybot,'w-',linewidth=2)
axa.plot(Xlft,Ylft,'w-',linewidth=2)
axa.plot(Xtop0,Ytop0,'w-',linewidth=2)
axa.plot(Xtop1,Ytop1,'w-',linewidth=2)
axa.plot(Xtop2,Ytop2,'w-',linewidth=2)
axa.plot(Xrig,Yrig,'w-',linewidth=2)
axa.plot(Xbot[0],Ybot[0],'wo')
axa.plot(Xlft[0],Ylft[-1],'wo')
axa.plot(Xtop0[-1],Ytop0[0],'wo')
axa.plot(Xtop1[0],Ytop1[-1],'wo')
axa.plot(Xtop2[-1],Ytop2[-1],'wo')
axa.plot(Xrig[-1],Yrig[0],'wo')


axb=fig.add_subplot(gs[0,1],projection=ccrs.PlateCarree())
axb.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
axb.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img10=axb.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='black',transform=ccrs.PlateCarree())
axb.clabel(img10,levels=levs,fontsize=12)
axb.add_feature(cfea.COASTLINE,edgecolor='white')
gl=axb.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
axb.set_title('Spring',color='g')
img01=axb.pcolormesh(XC,YC,PGBI[1,:,:],cmap='jet',vmin=0,vmax=60)
gl.top_labels=False
gl.bottom_labels=False
gl.left_labels=False
gl.right_labels=False
gl.xlines=True
axb.text(-70.5,42.75,'(b)')
axb.plot(Xbot,Ybot,'w-',linewidth=2)
axb.plot(Xlft,Ylft,'w-',linewidth=2)
axb.plot(Xtop0,Ytop0,'w-',linewidth=2)
axb.plot(Xtop1,Ytop1,'w-',linewidth=2)
axb.plot(Xtop2,Ytop2,'w-',linewidth=2)
axb.plot(Xrig,Yrig,'w-',linewidth=2)
axb.plot(Xbot[0],Ybot[0],'wo')
axb.plot(Xlft[0],Ylft[-1],'wo')
axb.plot(Xtop0[-1],Ytop0[0],'wo')
axb.plot(Xtop1[0],Ytop1[-1],'wo')
axb.plot(Xtop2[-1],Ytop2[-1],'wo')
axb.plot(Xrig[-1],Yrig[0],'wo')

axc=fig.add_subplot(gs[1,0],projection=ccrs.PlateCarree())
axc.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
axc.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img10=axc.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='black',transform=ccrs.PlateCarree())
axc.clabel(img10,levels=levs,fontsize=12)
axc.add_feature(cfea.COASTLINE,edgecolor='white')
gl=axc.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
axc.set_title('Summer',color='r')
img1=axc.pcolormesh(XC,YC,PGBI[2,:,:],cmap='jet',vmin=0,vmax=60)
gl.top_labels=False
gl.bottom_labels=True
gl.left_labels=True
gl.right_labels=False
gl.xlines=True
axc.text(-70.5,42.75,'(c)')
axc.plot(Xbot,Ybot,'w-',linewidth=2)
axc.plot(Xlft,Ylft,'w-',linewidth=2)
axc.plot(Xtop0,Ytop0,'w-',linewidth=2)
axc.plot(Xtop1,Ytop1,'w-',linewidth=2)
axc.plot(Xtop2,Ytop2,'w-',linewidth=2)
axc.plot(Xrig,Yrig,'w-',linewidth=2)
axc.plot(Xbot[0],Ybot[0],'wo')
axc.plot(Xlft[0],Ylft[-1],'wo')
axc.plot(Xtop0[-1],Ytop0[0],'wo')
axc.plot(Xtop1[0],Ytop1[-1],'wo')
axc.plot(Xtop2[-1],Ytop2[-1],'wo')
axc.plot(Xrig[-1],Yrig[0],'wo')

axd=fig.add_subplot(gs[1,1],projection=ccrs.PlateCarree())
axd.set_extent([-70,-65,39.5,42.5],crs=ccrs.PlateCarree())
axd.add_feature(cfea.NaturalEarthFeature('physical','land',color='gray',scale='10m',edgecolor='none'))
img11=axd.contour(lon,lat,H,levels=levs,linewidths=1.5,colors='black',transform=ccrs.PlateCarree())
axd.clabel(img10,levels=levs,fontsize=12)
axd.add_feature(cfea.COASTLINE,edgecolor='white')
gl=axd.gridlines(crs=ccrs.PlateCarree(),linewidth=2,color='black',alpha=0.5,linestyle='--',draw_labels=True)
axd.set_title('Fall',color='m')
img1=axd.pcolormesh(XC,YC,PGBI[3,:,:],cmap='jet',vmin=0,vmax=60)
gl.top_labels=False
gl.bottom_labels=True
gl.left_labels=False
gl.right_labels=False
gl.xlines=True
axd.text(-70.5,42.75,'(d)')
axd.plot(Xbot,Ybot,'w-',linewidth=2)
axd.plot(Xlft,Ylft,'w-',linewidth=2)
axd.plot(Xtop0,Ytop0,'w-',linewidth=2)
axd.plot(Xtop1,Ytop1,'w-',linewidth=2)
axd.plot(Xtop2,Ytop2,'w-',linewidth=2)
axd.plot(Xrig,Yrig,'w-',linewidth=2)
axd.plot(Xbot[0],Ybot[0],'wo')
axd.plot(Xlft[0],Ylft[-1],'wo')
axd.plot(Xtop0[-1],Ytop0[0],'wo')
axd.plot(Xtop1[0],Ytop1[-1],'wo')
axd.plot(Xtop2[-1],Ytop2[-1],'wo')
axd.plot(Xrig[-1],Yrig[0],'wo')

axf=fig.add_axes([0.2,0.08,0.35,0.02])
cbar=plt.colorbar(img1,cax=axf,orientation="horizontal")
custom_ticks=[0,20,40,60]
cbar.set_ticks(custom_ticks)
axf.set_xlabel('% Particles Remaining on Georges Bank at 102 Days (ref. initial location)')

axe=fig.add_subplot(gs[:,2])
axe.plot(tdy,PNGB1Dmean[:,0],'b-o',label='Winter ('+r'$t_{ef}=$'+ tPEFtxt[0] +' days)')
axe.plot(tdy,PNGB1Dmean[:,1],'g-o',label='Spring ('+r'$t_{ef}$'+'> 80 days)')
axe.plot(tdy,PNGB1Dmean[:,2],'r-o',label='Summer ('+r'$t_{ef}=$'+ tPEFtxt[1] +' days)')
axe.plot(tdy,PNGB1Dmean[:,3],'m-o',label='Fall ('+r'$t_{ef}=$'+ tPEFtxt[2] +' days)')
axe.legend()
axe.set_xticks([0,10,20,30,40,50,60,70,80])
axe.set_xticklabels(['0','10','20','30','40','50','60','70','80'])
axe.set_yticks([0,20,40,60,80,100])
axe.set_yticklabels(['0','20','40','60','80','100'])
axe.fill_between(tdy,PNGB1Dmean[:,0]-PNGB1Dstd[:,0],PNGB1Dmean[:,0]+PNGB1Dstd[:,0],color='b',alpha=0.1)
axe.fill_between(tdy,PNGB1Dmean[:,1]-PNGB1Dstd[:,1],PNGB1Dmean[:,1]+PNGB1Dstd[:,1],color='g',alpha=0.1)
axe.fill_between(tdy,PNGB1Dmean[:,2]-PNGB1Dstd[:,2],PNGB1Dmean[:,2]+PNGB1Dstd[:,2],color='r',alpha=0.1)
axe.fill_between(tdy,PNGB1Dmean[:,3]-PNGB1Dstd[:,3],PNGB1Dmean[:,3]+PNGB1Dstd[:,3],color='m',alpha=0.1)
axe.set_xlabel('Time in Days (ref. initial deployment date)')
axe.set_xlim(0,80)
axe.set_ylim(0,100)
axe.grid()
axe.text(-13,35,'% on Georges Bank',rotation=90) 
axe.text(-17,99,'(e)')

fig.savefig('figure3.png')
