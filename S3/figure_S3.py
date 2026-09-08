#! /usr/bin/env python 

import numpy as np 
import matplotlib.pyplot as plt 

tdays=np.arange(0,6000)*12.43/24
tN=366*3+365*6+103
t0=np.arange(0,tN,12.43/24)
t0dy=np.arange(0,t0[-1]+12.43/24,12.43/24)/365
t0yr=t0dy+2004
tyr=t0yr[:6000]

f=np.load('flux_of_drifters_into_OSR_SURFACE_1D.npz')
NSURb=f['NFLS1D'][:]
f.close()

f=np.load('flux_of_drifters_into_OSR_SUBSURFACE_1D.npz')
NSUBb=f['NFLS1D'][:]
f.close()

f=np.load('MAP_LARGE_40_EDDY.npz')
MAP3b=f['MAP'][61:-500]
f.close()

NSUR=NSURb[:6000]
NSUB=NSUBb[:6000]
MAP3=MAP3b[:6000]

fig,ax2=plt.subplots(nrows=1,ncols=1,figsize=(12,4))
ax2.plot(tyr,MAP3,'b-',label='MAP'+r'$_0$')
ax2.set_xlabel('Time (years ref. Jan 1, 2004)')
ax2.set_ylabel('Instantaneous Particle Flux')
ax2.grid()
ax=ax2.twinx()
ax.plot(tyr,NSUR,'r-',label='Flux of Surface Particles (R=0.04)')
jj=np.argmax(NSUR)
yy=np.arange(0,10000)
xx=tyr[jj]*np.ones(len(yy))
ax2.plot(xx,yy,'k-',linewidth=3)
ax.plot(tyr,NSUB,'g-',label='Flux of Depth Particles (R=0.16)')
ax2.set_ylabel('Maximum Advective Potential',color='b')
ax2.tick_params(axis='y',colors='b')
ax.set_ylabel('Instantaneous Flux of Particles')
handles1,labels1=ax2.get_legend_handles_labels()
handles2,labels2=ax.get_legend_handles_labels()
all_handles=handles1+handles2
all_labels=labels1+labels2
ax2.legend(all_handles,all_labels,loc='best')
ax2.set_xlim(2004,2012.5)
ax2.set_ylim(0,0.025)
ax.set_ylim(0,10000)
ax.text(tyr[jj],10500,'Nov. Event',horizontalalignment='center')
fig.savefig('figure_S3.png')

