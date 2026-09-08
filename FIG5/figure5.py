#! /usr/bin/env python 

import numpy as np
import matplotlib.pyplot as plt

# for WCRs with R > 40km
f=np.load('MAP_LARGE_40_EDDY.npz')
MAP3b=f['MAP'][61:-500]
f.close()
MAP=MAP3b[:6000]

# load number of particles on Georges Bank 
#surface deployed
f=np.load('Ndrifters_on_Georges_Bank_SURFACE.npz')
NtotSF=f['Ntot1D'][:6000] 
f.close()

#SUBsurface deployed
f=np.load('Ndrifters_on_Georges_Bank_SUBSURFACE.npz')
NtotSS=f['Ntot1D'][:6000] 
f.close()

# SURFACE FRACTIONAL flux into OSR (NFLS)
f=np.load('fractional_flux_into_OSR_ref_number_larave_on_Georges_Bank_SURFACE.npz')
FSUR=f['F'][:]
f.close()
f=np.load('fractional_flux_into_OSR_ref_number_larave_on_Georges_Bank_SUBSURFACE.npz') 
FSUB=f['F'][:]
f.close()

# plot progressive set of RUNNING averaging intervals
# ti is time in days
tN=366*3+365*6+103
t0=np.arange(0,tN,12.43/24)
t0dy=np.arange(0,t0[-1]+12.43/24,12.43/24)/365
t0yr=t0dy+2004
tyr=t0yr[:6000]

fig,ax=plt.subplots(nrows=2,ncols=1,figsize=(12,8))
ax[0].plot(tyr,NtotSF,'r',label='Surface Particles (mean= '+r'$16400 \pm 6500$'+', R=0.67)')
ax[0].plot(tyr,NtotSS,'g',label='Subsurface Particles (mean='+r'$23000 \pm 4900$'+')')
ax[0].plot(tyr,np.ones(len(tyr))*16400,'r--')
ax[0].plot(tyr,np.ones(len(tyr))*23000,'g--')
ax[0].legend(loc=1)

# add a vertical line for maximum value of FSUR (Nov event) 
jj=np.argmax(FSUR) 
yy=np.arange(0,40000)
xx=np.ones(len(yy))*tyr[jj]

ax[0].grid()
ax[0].set_ylabel('Number on GB')
ax[0].set_xlim(2004,2012.5)
ax[0].set_ylim(0,40000)
ax[0].text(2003.75,42500,'(a)')
ax[0].text(tyr[jj],42500,'Nov Event',horizontalalignment='center')
ax[0].plot(xx,yy,'k-',linewidth=3,alpha=0.75)

# add a vertical line for maximum value of FSUR (Nov event) 
jj=np.argmax(FSUR) 
yy2=np.arange(0,0.02,0.0001)
xx2=np.ones(len(yy2))*tyr[jj]

ax[1].plot(tyr,MAP,'b-',label=r'$MAP_0$')
ax[1].set_ylabel('MAP (' + r'$\text{km}^{-1}$'+')',color='b') 
ax[1].tick_params(axis='y',colors='b')
ax[1].set_ylim(0,0.02)
ax[1].plot(xx2,yy2,'k-',linewidth=3,alpha=0.75)
ax2=ax[1].twinx()
ax2.plot(tyr,FSUR,'r',label='Surface (mean='+r'$0.03 \pm 0.04$'+', R=0.07)')
ax2.plot(tyr,FSUB,'g',label='Subsurface (mean='+r'$0.007 \pm 0.005$'+', R=0.15)')
handles1,labels1=ax[1].get_legend_handles_labels()
handles2,labels2=ax2.get_legend_handles_labels()
all_handles=handles1+handles2
all_labels=labels1+labels2
ax2.legend(all_handles,all_labels,loc='best')
ax2.set_xlim(2004,2012.5)
ax2.grid()
ax2.set_xlabel('Calendar Year') 
ax2.set_ylabel('Fraction into OSR')
ax2.set_xlim(2004,2012.5)
ax2.text(2003.75,0.95,'(b)')
ax2.text(tyr[jj],0.95,'Nov Event',horizontalalignment='center')
ax2.set_ylim(0,0.9)
fig.savefig('figure5.png')
