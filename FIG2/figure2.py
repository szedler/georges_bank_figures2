#! /usr/bin/python env 
import numpy as np 
import matplotlib.pyplot as plt 

# load stats 
#dno='/Users/sarahzedler/darwin/scripts/github/GH1/'
f=np.load('retention_time_GB_statistics.npz')
tyr=f['tyr'][:]
QE=f['QE'][:]
tmth=f['tmth'][:]
QEmean1=f['QEmean1'][:]
QEmean2=f['QEmean2'][:]
QElo1=f['QElo1'][:]
QEhi1=f['QEhi1'][:]
QElo2=f['QElo2'][:]
QEhi2=f['QEhi2'][:]
tstr=f['tstr']
tmth=f['tmth']
f.close()

# Create the figure and subplots using subplot_mosaic
tyr2=np.arange(0,118)*30/360+2004
fig = plt.figure(constrained_layout=True, figsize=(10, 5)) # constrained_layout helps with spacing
axs = fig.subplot_mosaic([['left', 'upper_right'],
                          ['left', 'lower_right']])

axs['left'].plot(tyr2,QE,color='b',linestyle='-',marker='o')
axs['left'].set_xlabel('Deployment Date (in years, on first of each month)')
axs['left'].set_ylabel('Time (days)')
axs['left'].set_xlim(2004,2014)
axs['left'].grid()
axs['left'].text(2003.4,274,'(a)')

axs['upper_right'].plot(tmth,QEmean2,color='r',linestyle='-',marker='o')
axs['upper_right'].fill_between(tmth,QElo2,QEhi2,color='r',alpha=0.2)
axs['upper_right'].set_xticks(tmth)
axs['upper_right'].set_xticklabels(tstr)
axs['upper_right'].grid()
axs['upper_right'].set_xlim(0,11)
axs['upper_right'].set_xlabel('Deployment Date (all years)')
axs['upper_right'].set_title('Intraannual Distribution (N=9 years)')
axs['upper_right'].text(-0.7,255,'(b)')

axs['lower_right'].plot(tyr,QEmean1,'g-o')
axs['lower_right'].fill_between(tyr,QElo1,QEhi1,color='g',alpha=0.2)
axs['lower_right'].grid()
axs['lower_right'].set_xlim(2004,2012)
axs['lower_right'].set_xlabel('Year (N=12 months)')
axs['lower_right'].set_title('Interannual Distribution (N=12 months)')
axs['lower_right'].text(2003.4,220,'(c)')

fig.savefig('figure2.png')
