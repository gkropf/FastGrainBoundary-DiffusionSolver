#import os
#import sys
from numpy import *
import numpy.matlib
import matplotlib.pyplot as plt
import timeit
#Use FGB_03S1T1

#will read from gui
start_time=timeit.default_timer()
plot1=1
plot2=1
tim=timeit.default_timer()
total_time=0
time_solve=0

######## Fluxball function ######

def fluxbal(z,e,f,h,j,k,l):
    X=zeros([z])
    A=zeros([z,z])
    for m in range(0,z-1):
        A[m,0]=1
        A[m,m+1]=-1
    A[z-1,:]=j*k*l*f
    B=zeros([z])
    B[0:z-1]=h[1:z]
    B[z-1]=sum(j*k*l*f*e)
    X=linalg.solve(A,B)
    return X

######## Fluxball function #######

##### Octrave Function #######
def octrave(b):
    file = open(b, 'r')
    str = file.read()
    rows = str.split('\n')
    rowb=len(rows)
    colb=len(rows[0].split('\t'))
    dat=zeros([rowb, colb])
    for i in range(0, rowb):
         dat[i,:] = rows[i].split('\t')
    if colb==3:
        distance = dat[:,colb-1]
    else:
        print('et')
        X0 = dat[0,colb-2]
        Y0 = dat[0,colb-1]
        ##select traverse origin
        origin = zeros([colb])
        origin[colb-2] = X0
        origin[colb-1] = Y0
        OR = numpy.matlib.repmat(origin, rowb, 1)
        #referance all coordinates to newly selected origin
        C = dat - OR
        N = C[:,colb-2:colb]
        travend = C[rowb-1,colb-2:colb]
        distance=zeros([rowb])
        for i in range(0,rowb):
            distance[i] = dot(N[i,:],travend)/sqrt(pow(travend[0],2)+pow(travend[1],2))
    return [distance,dat[:,0],dat[:,1]]



##### Octrave Function #######





######### User Defined Info #########
ttot=4        #duration of model run in millions of years
dt=5e-4       #time step in m.y.
WRd180=12.8   #estimate of whole-rock d180
Tstart=700    #initial temp in C
Tend=500      #end temp in C
cool=1    #method of cooling
nmin=4        #num of minerals
de=100        #distance segments per grain
######### User Defined Info #########


######### Unit Definitions and Conversions ########
deltat = dt*3.1536e+13
tend=math.ceil(ttot/dt)
Tstart=Tstart+273
Tend=Tend+273
T0=Tstart
T=Tstart
######### Unit Definitions and Conversions ########


######### Initialize Storage Matrices #########
mode=zeros([nmin])
shape=zeros([nmin])
L=zeros([nmin])
w=zeros([nmin])
r=zeros([nmin])
SA=zeros([nmin])
dx=zeros([nmin])
gb=zeros([nmin])
d180=zeros([nmin])
Afac=zeros([nmin])
Bfac=zeros([nmin])
Cfac=zeros([nmin])
D0=zeros([nmin])
Q=zeros([nmin])
D=zeros([nmin])
fracfax=zeros([nmin])
oxcon=zeros([nmin])
R=8.3144621 #J/K*ml
######### Initialize Storage Matrices #########


######### Rock Descriptions #########
#mineral 1 - monitor, quartz
mode[0]=0.20
shape[0]=2
r[0]=20
L[0]=2*r[0]
w[0]=20
dx[0]=r[0]/de
gb[0]=math.ceil(L[0]/dx[0])
#X1=linspace(0,L[0],gb[0])
Afac[0]=0
Bfac[0]=0
Cfac[0]=0
d180[0]=99
D0[0]=3.4e-9
Q[0]=98000
oxcon[0]=0.0882

#mineral 2 - alkali feldspar
mode[1]=0.76
shape[1]=1
r[1]=30
L[1]=2*r[1]
w[1]=30
dx[1]=r[1]/de
gb[1]=math.ceil(L[1]/dx[1])
#X1=linspace(1,L[1],gb[1])
Afac[1]=0
Bfac[1]=0
Cfac[1]=1.0
d180[1]=99
D0[1]=7.6e-6
Q[1]=129500
oxcon[1]=0.0734

#mineral 3 - titanite
mode[2]=0.01
shape[2]=1
r[2]=450
L[2]=2*r[2]
w[2]=700
dx[2]=r[2]/de
gb[2]=math.ceil(L[2]/dx[2])
#X1=linspace(2,L[2],gb[2])
Afac[2]=0
Bfac[2]=0
Cfac[2]=3.66
d180[2]=99
D0[2]=2.05e-8
Q[2]=180000
oxcon[2]=0.0874

#mineral 4 - augite
mode[3]=0.03
shape[3]=1
r[3]=30
L[3]=2*r[3]
w[3]=30
dx[3]=r[3]/de
gb[3]=math.ceil(L[3]/dx[3])
#X1=linspace(3,L[3],gb[3])
Afac[3]=0
Bfac[3]=0
Cfac[3]=2.75
d180[3]=99
D0[3]=1.5e-6
Q[3]=226000
oxcon[3]=0.0892
######### Rock Descriptions ########

##################################################################temp
gb=gb+1

#convert input to micron
L=L*1e-4
w=w*1e-4
r=r*1e-4
dx=dx*1e-4
maxdim=max(gb)

#normalize mineral modes
mode=mode.copy()/sum(mode)

#calculate mineral surface area
for m in range(0,nmin):
  if shape[m]==1:
    SA[m]=(4*pi*pow(r[m],2))
  else:
    if shape[m]==2:
       SA[m]=2*L[m]*w[m]
    else:
       SA[m]=2*upi*r[m]*h[m]

print('Check166')
#initial conditions (starting concentration profiles)
for m in range(0,nmin):
    fracfax[m] = Afac[m] + ((Bfac[m]*1e3)/T0) + ((Cfac[m]*1e6)/pow(T0,2))

print('Check171')
#recalculate estimated whole rock based on disequilibrium phase (only works
#for one diseq phase in this formulation; preferrably a low-volume/accessory phase)
for m in range(0,nmin):
    if d180[m] < 99:
        WRd180 = WRd180*(1-mode[m])+ d180[m]*mode

d180mon=WRd180+dot(mode,fracfax)
print('Check179')
gbvalinit=zeros([nmin])
for m in range(0,nmin):
    gbvalinit[m] = d180mon - fracfax[m]
print('Check183')
Told = zeros([nmin,int(max(gb))])
for m in range(0,nmin):
    if d180[m] == 99:
        Told[m,0:int(gb[m])] = gbvalinit[m]
    ###################elseif d18O == 100 %load precursor profile from text file
    #################### Told(m) = reshape(load(uigetfile('*.txt')),1,1:gb(m))
    else:
        Told[m,0:int(gb[m])] = d180[m]

#### Solve fully implicit
#####define data storage matrices
time=zeros([tend])
Temphx=zeros([tend])
Tnew=zeros([nmin,int(max(gb))])
pregbval = zeros([nmin])
result = zeros([nmin,tend,int(maxdim)])  #array for storing results for all
                                         #minerals, indices (m,t,i)
DTdt=zeros([tend])



for t in range(0,int(tend)):
  if cool == 1:
     DTdt = (Tstart-Tend)/ttot   #linear in t
     T = T0 - (DTdt*(t+1)*dt)
  else:
     k = ttot/((1/Tend)-(1/Tstart))
     T = 1/((((t+1)*dt)/k)+(1/Tstart))
  D=D0*exp(-Q/(R*T))
  fracfax=Afac+Bfac*(1e3/T)+Cfac*(1e6/pow(T,2))
  coeff=D/dx
###checked to here good #################################################################################
  for m in range(0,nmin):
        if shape[m]==1:     #spherical/isotropic diffusion geometry
            gb[m] = math.ceil(r[m]/dx[m])+1
            a = ones([int(gb[m])])
            a[int(gb[m])-1] = 2
            b=(-2-((dx[m]*dx[m]))/(D[m]*deltat))*ones([int(gb[m])])
            c = ones([int(gb[m])])
            c[0] = 2
            d = -((dx[m]*dx[m])/(D[m]*deltat))*Told[m,0:int(gb[m])]
            for i in range(1,int(gb[m])-1):
                 a[i] = (i-1)/i
                 c[i] = (i + 1)/i
        else: #slab/infinite plane diffusion geometry
            a = ones([int(gb[m])])
            a[int(gb[m])-1] = 2
            b = (-2-((dx[m]*dx[m]))/(D[m]*deltat))*ones([int(gb[m])])
            c = ones([int(gb[m])])
            c[0] = 2
            d =-((dx[m]*dx[m])/(D[m]*deltat))*Told[m,0:int(gb[m])]
        TD = diag(b)+diag(a[1:],-1)+diag(c[0:-1],1)
        total_time=total_time+timeit.default_timer()-tim
        tim=timeit.default_timer()
        Tnew[m,0:int(gb[m])]=linalg.solve(TD,d)
        time_solve=time_solve+timeit.default_timer()-tim
        tim=timeit.default_timer()
        pregbval[m]=Tnew[m,int(gb[m])-1]
        #print(pregbval)
        #input("")
        #c=diag(b)
        #print(c[0,:])
        #input("")
        #c=diag(a[1:],-1)
        #print(c[0,:])
        #input("")
        #k=diag(c[0:-1],1)
        #print(k[0,:])
        #input("")
        ################good bad line
        #print(TD[0,:])
        #input("")
  gbval=fluxbal(nmin,pregbval,coeff,fracfax,mode,SA,oxcon)
  for m in range(0,nmin):
      Tnew[m,int(gb[m])-1]=gbval[m]
      if shape[m]==2:
          Tnew[m,1]=gbval[m]
      Told[m,:]=Tnew[m,:]
      time[t]=t*dt
      Temphx[t]=T
      result[m,t,0:int(gb[m])]=Told[m,0:int(gb[m])]

if plot1==1:
    #loc1 = os.path.dirname(sys.argv[0])
    #loc1 = loc1 + '/HA03_S1_T1.txt'
    loc1 = 'C:/Users/gabe_/Documents/PyCharm/HA03_S1_T1.txt'
    y=result[2,tend-1,0:int(gb[2])].reshape(1,int(gb[2]))
    a = octrave(loc1)
    plt.figure(1)
    plt.errorbar(a[0], a[1], a[2], fmt='o')
    u=471  #distance in m
    u=u*1e-4
    a=y[0:int(gb[2])-1]
    uvec = 1e4*linspace(u,r[2]+u-dx[2],int(gb[2]))
    plt.plot(uvec,a[0,:],'k-')
    v=52
    v=v*1e-4
    vvec = 1e4*linspace(v,r[2]+v-dx[2],int(gb[2]))
    plt.plot(vvec,a[0,::-1],'k-')

if plot2==1:
    plt.figure(2)
    for t in [0,tend-2]:
        if t==0:
            st='r-'
        else:
            st='b-'


        y=result[:,int(t),:].reshape(int(nmin),int(maxdim))
        for m in range(0,nmin):
            plt.subplot(nmin,1,m+1)
            tg=int(gb[m])
            if shape[m]==1:
                plt.plot(1e4*linspace(r[m],2*r[m]-dx[m],tg),y[m,0:tg], st)
                plt.plot(1e4*linspace(r[m],dx[m],tg),y[m,0:tg], st)
            else:
                plt.plot(1e4*linspace(dx[m],L[m]-dx[m],tg),y[m,0:tg], st)

    plt.show()

print(time_solve,total_time)
print(timeit.default_timer()-start_time)
