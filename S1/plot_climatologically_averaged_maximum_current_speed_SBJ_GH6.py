#! /usr/bin/env python 
import numpy as np
import matplotlib.pyplot as plt

dn='/Users/sarahzedler/darwin/scripts/github/FIG6/'
f=np.load(dn+'climatological_seasonally_averaged_position_maximum_SBJ.npz')
lont2=f['LONsea'][:]
latt2=f['LATsea'][:]
St2=f['Ssea'][:]
Sstd2=f['Sstd'][:]
Sse2=f['Sse'][:]
f.close()


fig,ax = plt.subplots(figsize=(8.5,6))
ax.plot(lont2[0,:],St2[0,:],'b-o',label='Winter',linewidth=2)
ax.plot(lont2[1,:],St2[1,:],'g-o',label='Spring',linewidth=2)
ax.plot(lont2[2,:],St2[2,:],'r-o',label='Summer',linewidth=2)
ax.plot(lont2[3,:],St2[3,:],'m-o',label='Fall',linewidth=2)
ax.legend(fontsize=15)
ax.grid()
ax.set_xlabel('Longitude',fontsize=15) 
ax.set_ylabel('Speed (m/s)',fontsize=15)
ax.set_xlim(-69,-66)
ax.set_xticks([-69,-68,-67,-66])
ax.set_xticklabels(['69W','68W','67W','66W'],fontsize=15)
ax.set_ylim(0.2,0.6)
ax.set_yticks([0.25,0.35,0.45,0.55]) 
ax.set_yticklabels(['0.25','0.35','0.45','0.55'],fontsize=15)

dno='/Users/sarahzedler/darwin/scripts/github/FIG6/'
fig.savefig(dno+'climatological_mean_maximum_SBJ.png')
