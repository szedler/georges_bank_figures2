#! /usr/bin/env python 

import numpy as np 
import matplotlib.pyplot as plt 

labs0=[r'$MAP_4$',r'$MAP_5$',r'$MAP_0$',r'$MAP_1$',r'$MAP_2$',r'$MAP_3$']

f=np.load('correlations_SURFACE2.npz')
NFtime=f['NFtime'][:]
Nt=f['Nt'][:]
tyr=f['tyr'][:]
f.close()

f=np.load('correlations_cenedese_SURFACE2.npz')
#Nt=f['Nt'][:]
CC=f['CC'][:]
CC2=f['CC2'][:]
C0=f['C0'][:]
C1=f['C1'][:]
C2=f['C2'][:]
C3=f['C3'][:]
f.close()

f=np.load('correlations_SUBSURFACE2.npz')
NFtimeb=f['NFtimeb'][:]
Ntb=f['Ntb'][:]
f.close()

f=np.load('correlations_cenedese_SUBSURFACE2.npz')
CCb=f['CCb'][:]
CCb2=f['CCb2'][:]
C0b=f['C0b'][:]
C1b=f['C1b'][:]
C2b=f['C2b'][:]
C3b=f['C3b'][:]
f.close()

f=np.load('confidence_intervals_SURFACE2.npz')
CLO=f['CLO'][:]
CHI=f['CHI'][:]
C=f['C'][:]
f.close()

f=np.load('confidence_intervals_SUBSURFACE2.npz')
CLOb=f['CLOb'][:]
CHIb=f['CHIb'][:]
Cb=f['Cb'][:]
dn='/Users/sarahzedler/darwin/scripts/georges_bank_figures2/FIG6/FIG6_INP_CO/'
f.close()

xticks=np.arange(0,210,50)
xticklabs=['0','50','100','150','200']
yticks0=np.arange(-0.25,1.2,0.25)
yticklabs0=['-0.25','0','0.25','0.5','0.75','1']
yticks1=np.arange(0.05,0.6,0.2)
yticklabs1=['0.05','0.25','0.45']

ZERO=np.zeros((len(Nt)))


# hardwiring the time step number for the Nov. event 
yy=np.arange(0,0.26,0.01)
xx=np.ones(len(yy))*tyr[1313]

yy2=np.arange(0,0.031,0.001)
xx2=np.ones(len(yy2))*tyr[1313]

fig,ax=plt.subplots(nrows=2,ncols=2,figsize=(12,8))
ax[0,0].plot(xx,yy,'k-',linewidth=3)
ax[0,0].text(xx[0],0.273,'Nov. Event',horizontalalignment='center')
ax[0,0].plot(tyr,NFtime[0,:],label=str(Nt[0])[:3]+' Days')
ax[0,0].plot(tyr,NFtime[22,:],label=str(Nt[22])[:4]+' Days')
ax[0,0].plot(tyr,NFtime[51,:],label=str(Nt[51])[:4]+ ' Days')
ax[0,0].plot(tyr,NFtime[167,:],label=str(Nt[167])[:4]+ ' Days')
ax[0,0].set_ylabel('Fractional Particle Flux')
ax[0,0].grid()
ax[0,0].legend()
ax[0,0].set_xlabel('Time (years ref. Jan 1, 2004)')
ax[0,0].set_ylim(0,0.25)
ax[0,0].set_xlim(2004,2012.5)
ax[0,0].text(2003.75,0.275,'(a)')

ax[0,1].plot(xx2,yy2,'k-',linewidth=3)
ax[0,1].text(xx2[0],0.031,'Nov. Event',horizontalalignment='center')
ax[0,1].plot(tyr,NFtimeb[0,:],label=str(Nt[0])[:3]+' Days')
ax[0,1].plot(tyr,NFtimeb[22,:],label=str(Nt[22])[:4]+' Days')
ax[0,1].plot(tyr,NFtimeb[51,:],label=str(Nt[51])[:4]+ ' Days')
ax[0,1].plot(tyr,NFtimeb[167,:],label=str(Nt[167])[:4]+ ' Days')
ax[0,1].set_xlabel('Time (years ref. Jan 1, 2004)')
ax[0,1].grid()
ax[0,1].set_ylim(0,0.03)
ax[0,1].set_xlim(2004,2012.5)
ax[0,1].text(2003.75,0.032,'(b)')

ax[1,0].plot(Nt,C0,'b-',label=labs0[2])
ax[1,0].plot(Nt,C1,'g-',label=labs0[3])
ax[1,0].plot(Nt,C2,'r-',label=labs0[4])
ax[1,0].plot(Nt,C3,'c-',label=labs0[5])
ax[1,0].plot(Nt,CC,'m-',label=labs0[0])
ax[1,0].plot(Nt,CC2,'y-',label=labs0[1])
ax[1,0].fill_between(Nt,CLO[2,:],CHI[2,:],color='b',alpha=0.1)
ax[1,0].fill_between(Nt,CLO[3,:],CHI[3,:],color='g',alpha=0.1)
ax[1,0].fill_between(Nt,CLO[4,:],CHI[4,:],color='r',alpha=0.1)
ax[1,0].fill_between(Nt,CLO[5,:],CHI[5,:],color='c',alpha=0.1)
ax[1,0].fill_between(Nt,CLO[0,:],CHI[0,:],color='m',alpha=0.1)
ax[1,0].fill_between(Nt,CLO[1,:],CHI[1,:],color='y',alpha=0.1)
ax[1,0].plot(Nt,ZERO,'k--',linewidth=2)
ax[1,0].set_ylabel('Correlation Coefficient')
ax[1,0].grid()
ax[1,0].legend()
ax[1,0].set_xlabel('Time Period for Correlation (in days)')
ax[1,0].set_xlim(0,200)
ax[1,0].text(-6,1.1,'(c)')
ax[1,0].set_xticks(xticks)
ax[1,0].set_xticklabels(xticklabs)
ax[1,0].set_yticks(yticks0)
ax[1,0].set_yticklabels(yticklabs0)
ax[1,0].set_xlim(Nt[0],Nt[-1])
ax[1,0].set_ylim(-0.25,1)
ax[1,0].plot(xx2,yy2,'k-',linewidth=3)

ax[1,1].plot(Nt,C0b,'b-',label='MAP(all R)/NFL')
ax[1,1].plot(Nt,C1b,'g-',label='MAP(R>20km)/NFL')
ax[1,1].plot(Nt,C2b,'r-',label='MAP2(R in [40,100]km)/NFL')
ax[1,1].plot(Nt,C3b,'c-',label='MAP3(R > 40km)/NFL')
ax[1,1].plot(Nt,CCb,'m-',label='MAP(all R)/NFL')
ax[1,1].plot(Nt,CCb2,'y-',label='MAP(all R)/NFL')
ax[1,1].fill_between(Nt,CLOb[2,:],CHIb[2,:],color='b',alpha=0.1)
ax[1,1].fill_between(Nt,CLOb[3,:],CHIb[3,:],color='g',alpha=0.1)
ax[1,1].fill_between(Nt,CLOb[4,:],CHIb[4,:],color='r',alpha=0.1)
ax[1,1].fill_between(Nt,CLOb[5,:],CHIb[5,:],color='c',alpha=0.1)
ax[1,1].fill_between(Nt,CLOb[0,:],CHIb[0,:],color='m',alpha=0.1)
ax[1,1].fill_between(Nt,CLOb[1,:],CHIb[1,:],color='y',alpha=0.1)
ax[1,1].set_xlabel('Time Period for Correlation (in days)')
ax[1,1].grid()
ax[1,1].set_xlim(0,200)
ax[1,1].set_ylim(0.1,0.6)
ax[1,1].text(-6,1.1,'(d)')
ax[1,1].set_xticks(xticks)
ax[1,1].set_xticklabels(xticklabs)
ax[1,1].set_yticks(yticks0)
ax[1,1].set_yticklabels(yticklabs0)
ax[1,1].set_xlim(Nt[0],Nt[-1])
ax[1,1].set_ylim(-0.25,1)
ax[1,1].plot(Nt,ZERO,'k--',linewidth=2)

fig.savefig('figure6.png')

