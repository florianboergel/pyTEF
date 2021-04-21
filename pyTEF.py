"""
python package to compute the total exchange flow (TEF) properties (MacCready, 2011) with the dividing salinity method ( Lorenz et al., 2019) and the T-S decomposition as presented in Lorenz et al. (2020)
"""

import numpy as np
import xarray as xr

def calc_bulk_values(data,coord='salt_Q',Q='Q',min_trans='auto'):
    
    ###
    # function to compute the bulk values from a Q profile
    ###
    
    #load data as np.array
    coord = np.array(getattr(data,coord))
    Qv = np.array(getattr(data,Q))
    
    smin=coord[0]
    DeltaS=coord[1]-coord[0]
    
    if min_trans == 'auto':
        min_trans=0.01*np.max(np.abs(Qv))
    
    if len(Qv.shape) > 1:
        #first dimension is time! -> keep this dimension!
        
        #prepare storage arrays for Qin, Qout, consider multiple inflow/outflows! 
        Qin_ar = np.zeros((Qv.shape[0],10)) #10 is the dummy length
        Qout_ar = np.zeros((Qv.shape[0],10))
        divsal_ar = np.zeros((Qv.shape[0],11)) #if there are 10 transports there would be 11 dividing salinities
        
        for t in np.arange(Qv.shape[0]):
            ind,minmax = find_extrema(Qv[t],min_trans)
            print(ind,minmax)
            div_sal=[]
            i=0
            while i < len(ind):
                    #print(Qvl[ind[i]])
                div_sal.append(smin+DeltaS*ind[i])
                i+=1
                    #print(smin+dss*ind[i])
                #calculate transports etc.
            Q_in_m=[]
            Q_out_m=[]
            index=[]
            i=0
            while i < len(ind)-1:
                Q_i=-(Qv[ind[i+1]]-Qv[ind[i]])
                if Q_i<0:
                    Q_out_m.append(Q_i)
                elif Q_i > 0:
                    Q_in_m.append(Q_i)
                else:
                    index.append(i)
                i+=1
            div_sal = np.delete(div_sal, index)
            print(div_sal)
            print(Q_in_m)
            print(Q_out_m)
            
            #storing results
            for i,qq in enumerate(Q_in_m):
                Qin_ar[t,i] = qq
            for i,qq in enumerate(Q_out_m):
                Qout_ar[t,i] = qq
            for i,ss in enumerate(div_sal):
                divsal_ar[t,i] = ss
            #create a xarray Dataset for the results
        ds = xr.Dataset(
        {
            "Qin": (["time", "m"], Qin_ar),
            "Qout": (["time", "m"], Qout_ar),
            "divsal": (["time", "n"], divsal_ar),
        },
        coords={
            "time": (["time"],data.time.values),
            "m": (["m"],np.arange(10)),
            "n": (["n"],np.arange(11)),
        },
        )
    
    else:
    
        print('min_trans',min_trans)
        ind,minmax = find_extrema(Qv,min_trans)
        print(ind,minmax)
        div_sal=[]
        i=0
        while i < len(ind):
                #print(Qvl[ind[i]])
            div_sal.append(smin+DeltaS*ind[i])
            i+=1
                #print(smin+dss*ind[i])
            #calculate transports etc.
        Q_in_m=[]
        Q_out_m=[]
        index=[]
        i=0
        while i < len(ind)-1:
            Q_i=-(Qv[ind[i+1]]-Qv[ind[i]])
            if Q_i<0:
                Q_out_m.append(Q_i)
            elif Q_i > 0:
                Q_in_m.append(Q_i)
            else:
                index.append(i)
            i+=1
        div_sal = np.delete(div_sal, index)
        print(div_sal)
        print(Q_in_m)
        print(Q_out_m)
    
    
    return(ds)
    #return(Q_in_m,Q_out_m,div_sal,ind)

def sort_2dim_xarray(data,dim=['salt','temp'],var=['flux'],N=256,dim_arrays = 'auto'):
    
    ##################
    #algorithm to sort the fluxes into a discrete 2D-array (typically salt ad temperature)
    # and give a xarray dataset as output
    ##################
    
    salt = getattr(data,dim[0])
    temp = getattr(data,dim[1])
    flux = getattr(data, var[0])
    if len(var)>1:
        for i in np.arange(1,len(var)):
            print(i)
            flux = flux*getattr(data,var[i])
    
    #convert the xarray dataframes into numpy arrays
    salt=np.array(salt.values)
    temp=np.array(temp.values)
    flux=np.array(flux.values)
    #mask invalid values
    salt=np.ma.masked_invalid(salt)
    temp=np.ma.masked_invalid(temp)
    flux=np.ma.masked_invalid(flux)
    
    print(salt.shape, flux.shape)
    if np.shape(salt)==np.shape(flux):
        print('input is good')
    else:
        sys.exit('sorting dimension and flux dont have the same dimension!')
        
    if dim_arrays == 'auto':
        #calculate number of salinity classes and create an array accordingly
        s_min = np.float64(np.min(salt))
        s_max = np.float64(np.max(salt))
        #print(s_min,s_max)
        Nmax = N
        #DeltaS = np.float64((s_max-s_min)/Nmax)
        s_min=int(s_min)
        s_max=int(s_max)+1
        
        t_min = np.float64(np.min(temp))
        t_max = np.float64(np.max(temp))
        Mmax = N
        t_min=int(t_min)
        t_max=int(t_max)+1
    else:
        salintiy_array=dim_arrays[0]
        temp_array=dim_arrays[1]
        s_min=salinity_array[0]
        s_max=salinity_array[-1]
        Nmax = len(salinity_array)
        t_min=temp_array[0]
        t_max=temp_array[-1]
        Mmax=len(temp_array)
        #DeltaS = np.float64((s_max-s_min)/Nmax)

    
    if np.ma.max(salt)> s_max:
        print('Warning: s > s_max found', np.max(salt),s_max)
    if np.ma.min(salt)< s_min:
        print('Warning: s < s_min found', np.min(salt),s_min)
    
    if np.ma.max(temp)> t_max:
        print('Warning: t > t_max found', np.max(temp),t_max)
    if np.ma.min(temp)< t_min:
        print('Warning: t < t_min found', np.min(temp),t_min)
    
    DeltaS = np.float64((s_max-s_min)/float(Nmax))
    s_q=np.arange(s_min+0.5*DeltaS,s_max+0.5*DeltaS,DeltaS)
    
    DeltaT= np.float64((t_max-t_min)/float(Mmax))
    t_q=np.arange(t_min+0.5*DeltaT,t_max+0.5*DeltaT,DeltaT)
   
    #define qv and qs:

    #keep the time axis
    time_max=salt.shape[0]
    print(time_max)
    qv = np.zeros(shape=(time_max,Nmax+1,Mmax+1),dtype=np.float64) 
    flux=np.ma.masked_where(np.ma.getmask(salt),flux)

    for t in np.arange(time_max):
        salt_tmp=np.ma.compressed(salt[t])
        temp_tmp=np.ma.compressed(temp[t])
        flux_tmp=np.ma.compressed(flux[t])

        idx=(salt_tmp-s_min)/DeltaS #compute the index in which the flux will be stored
        idx=idx.astype(int)+1
        idy=(temp_tmp-t_min)/DeltaT #compute the index in which the flux will be stored
        idy=idy.astype(int)+1
        for ii in np.arange(len(flux_tmp)):
            #idx = int((salt[ii]-s_min)/DeltaS)+1 #find the suiting salinity class
            qv[t,idx[ii],idy[ii]] += flux_tmp[ii]/DeltaS/DeltaT
            ii+=1

    qv=qv[:,1:,1:]
        
    #create a xarray Dataset for the results
    ds = xr.Dataset(
    {
        "q": (["time", dim[0]+"_q", dim[1]+"_q"], qv),
    },
    coords={
        "time": (["time"],data.time.values),
        dim[0]+"_q": ([dim[0]+"_q"],s_q),
        dim[1]+"_q": ([dim[1]+"_q"],t_q),
    },
    )
    
    return(ds)

def sort_1dim_xarray(data,dim='salt',var=['flux'],N=1024,salinity_array='auto'):
    
    ##################
    #algorithm to sort the fluxes into a discrete 1D-array (typically salt)
    # and give a xarray dataset as output
    ##################
    
    salt = getattr(data, dim)
    flux = getattr(data, var[0])
    if len(var)>1:
        for i in np.arange(1,len(var)):
            print(i)
            flux = flux*getattr(data,var[i])
    
    #convert the xarray dataframes into numpy arrays
    salt=np.array(salt.values)
    flux=np.array(flux.values)
    #mask invalid values
    salt=np.ma.masked_invalid(salt)
    flux=np.ma.masked_invalid(flux)
    
    print(salt.shape, flux.shape)
    if np.shape(salt)==np.shape(flux):
        print('input is good')
    else:
        sys.exit('sorting dimension and flux dont have the same dimension!')
        
    if salinity_array == 'auto':
        #calculate number of salinity classes and create an array accordingly
        s_min = np.float64(np.min(salt))
        s_max = np.float64(np.max(salt))
        #print(s_min,s_max)
        Nmax = N
        #DeltaS = np.float64((s_max-s_min)/Nmax)
        s_min=int(s_min)
        s_max=int(s_max)+1
    else:
        s_min=salinity_array[0]
        s_max=salinity_array[-1]
        Nmax = len(salinity_array)
        #DeltaS = np.float64((s_max-s_min)/Nmax)

    
    if np.ma.max(salt)>s_max:
        print('Warning: s > s_max found', np.max(salt),s_max)
    if np.ma.min(salt)<s_min:
        print('Warning: s < s_min found', np.min(salt),s_min)
    
    DeltaS = np.float64((s_max-s_min)/float(Nmax))
    s_q=np.arange(s_min+0.5*DeltaS,s_max+0.5*DeltaS,DeltaS)
    s_Q=np.arange(s_min,s_max+DeltaS,DeltaS)

    #define qv and qs:

    #keep the time axis
    tmax=salt.shape[0]
    print(tmax)
    qv = np.zeros(shape=(tmax,Nmax+1),dtype=np.float64) 
    flux=np.ma.masked_where(np.ma.getmask(salt),flux)

    for t in np.arange(tmax):
        salt_tmp=np.ma.compressed(salt[t])
        flux_tmp=np.ma.compressed(flux[t])

        idx=(salt_tmp-s_min)/DeltaS #compute the index in which the flux will be stored
        idx=idx.astype(int)+1
        for ii in np.arange(len(flux_tmp)):
            #idx = int((salt[ii]-s_min)/DeltaS)+1 #find the suiting salinity class
            qv[t,idx[ii]] += flux_tmp[ii]/DeltaS
            ii+=1

    qv=qv[:,1:]

    #Calculation of Qv:
    Qv = np.zeros((tmax,np.shape(qv)[1]+1))
    for i in np.arange(qv.shape[1]): #calculate Q(s) and Q_s(s)
        Qv[:,i]=np.sum(qv[:,i:]*DeltaS)
        
    #create a xarray Dataset for the results
    ds = xr.Dataset(
    {
        "q": (["time", dim+"_q"], qv),
        "Q": (["time", dim+"_Q"], Qv),
    },
    coords={
        "time": (["time"],data.time.values),
        dim+"_q": ([dim+"_q"],s_q),
        dim+"_Q": ([dim+"_Q"],s_Q),        
    },
    )
    
    return(ds)


def sort_1dim(salt,flux,keep_time=False,N=1024,salinity_array='auto',time_array=None):
    
    ##################
    #algorithm to sort the fluxes into a discrete 1D-array (typically salt)
    ##################
    
    #convert the xarray dataframes into numpy arrays
    salt=np.array(salt.values)
    flux=np.array(flux.values)
    #mask invalid values
    salt=np.ma.masked_invalid(salt)
    flux=np.ma.masked_invalid(flux)
    
    print(salt.shape, flux.shape)
    if np.shape(salt)==np.shape(flux):
        print('input is good')
    else:
        sys.exit('sorting dimension and flux dont have the same dimension!')
        
    if salinity_array == 'auto':
        #calculate number of salinity classes and create an array accordingly
        s_min = np.float64(np.min(salt))
        s_max = np.float64(np.max(salt))
        #print(s_min,s_max)
        Nmax = N
        #DeltaS = np.float64((s_max-s_min)/Nmax)
        s_min=int(s_min)
        s_max=int(s_max)+1
    else:
        s_min=salinity_array[0]
        s_max=salinity_array[-1]
        Nmax = len(salinity_array)
        #DeltaS = np.float64((s_max-s_min)/Nmax)

    
    if np.ma.max(salt)> s_max:
        print('Warning: s > s_max found', np.max(salt),s_max)
    if np.ma.min(salt)< s_min:
        print('Warning: s < s_min found', np.min(salt),s_min)
    
    DeltaS = np.float64((s_max-s_min)/float(Nmax))
    s_q=np.arange(s_min+0.5*DeltaS,s_max+0.5*DeltaS,DeltaS)
    s_Q=np.arange(s_min,s_max+DeltaS,DeltaS)

    #define qv and qs:
    if not keep_time:
        tmax=salt.shape[0]
        qv = np.zeros(shape=(Nmax+1,),dtype=np.float64) #+1 one to be easily able to compute Q which has the dimension Nmax+1, qv final dimension is (Nmax)

        #delete masked values with .compressed() (deletes masked values and flattens the array)
        salt=np.ma.compressed(salt)
        flux=np.ma.compressed(flux)

        print(salt.max(),salt.min(),s_min,s_max)
        
        idx=(salt-s_min)/DeltaS #compute the index in which the flux will be stored
        idx=idx.astype(int)+1
        for ii in np.arange(len(flux)):
            #idx = int((salt[ii]-s_min)/DeltaS)+1 #find the suiting salinity class
            qv[idx[ii]] += flux[ii]/DeltaS/tmax
            ii+=1
        qv=qv[1:]
        #Calculation of Qv:
        Qv = np.zeros((np.shape(qv)[0]+1,))
        for i in range(0,int(len(qv))): #calculate Q(s) and Q_s(s)
            Qv[i]=np.sum(qv[i:]*DeltaS)
    
    elif keep_time:
        #keep the time axis
        tmax=salt.shape[0]
        print(tmax)
        qv = np.zeros(shape=(tmax,Nmax+1),dtype=np.float64) 
        flux=np.ma.masked_where(np.ma.getmask(salt),flux)
        
        for t in np.arange(tmax):
            salt_tmp=np.ma.compressed(salt[t])
            flux_tmp=np.ma.compressed(flux[t])
        
            idx=(salt_tmp-s_min)/DeltaS #compute the index in which the flux will be stored
            idx=idx.astype(int)+1
            for ii in np.arange(len(flux_tmp)):
                #idx = int((salt[ii]-s_min)/DeltaS)+1 #find the suiting salinity class
                qv[t,idx[ii]] += flux_tmp[ii]/DeltaS
                ii+=1
                
        qv=qv[:,1:]
        
        #Calculation of Qv:
        Qv = np.zeros((tmax,np.shape(qv)[0]+1))
        for i in range(0,int(qv.shape[1])): #calculate Q(s) and Q_s(s)
            Qv[:,i]=np.sum(qv[:,i:]*DeltaS)
        
    #create a xarray Dataset for the results
    
    
    return(qv, Qv, s_q, s_Q)


def find_extrema(x,min_transport):
    """
    x: Q(S)
    min_transport: Q_thresh
    """
    if np.count_nonzero(x)==0:
        indices=[0]
        minmax=[0]
        return(indices,minmax)
    else:
        ###
        #set a minimum value to get rid of numerical noise
        ###
        if min_transport<=10**(-10):
            min_transport=10**(-10)

        ####
        #finding all extrema by evaluating each data point
        ####
        
        comp=1
        indices = []
        minmax = []
        i = 0
        while i < np.shape(x)[0]:
            if i-comp < 0:
                a = 0
            else:
                a=i-comp
            if i+comp+1>=len(x):
                b=None
                #c=i
            else:
                b=i+comp+1
                #c=b
            if x[i] == np.max(x[a:b]) and np.max(x[a:b]) != np.min(x[a:b]):# and x[i] != x[a]:
                indices.append(i)
                minmax.append('max')
            elif x[i] == np.min(x[a:b]) and np.max(x[a:b]) != np.min(x[a:b]):# and (x[i] != x[c] or x[i] != x[a]):
                indices.append(i)
                minmax.append('min')
            i+=1
        #print(indices,minmax)
        #print(x[indices])
        
        ###
        #correct consecutive extrema of the same kind, e.g., min min min or max max max (especially in the beginning and end of the salinity array)
        ###
        
        #index=[]
        ii=1
        while ii < len(indices):
            #print('minmin/maxmax',ii,len(indices))
            #print(minmax)
            index=[]
            if minmax[ii] == minmax[ii-1]:
                if minmax[ii] == 'max': #note the index of the smaller maximum
                    if x[indices[ii]]>=x[indices[ii-1]]:
                        index.append(ii-1)
                    else:
                        index.append(ii)
                elif minmax[ii] == 'min': #note the index of the greater minimum
                    if x[indices[ii]]<=x[indices[ii-1]]:
                        index.append(ii-1)
                    else:
                        index.append(ii)
                minmax = np.asarray(minmax)
                indices = np.asarray(indices)
                indices = np.delete(indices, index)
                minmax = np.delete(minmax, index)
            else:
                ii+=1
        #print(indices,minmax)
        
        ####
        #delete too small transports
        ####
        
        #print(indices,minmax)
        ii=0
        while ii < len(indices)-1: 
            index=[]
            #print('min_trans',ii,len(indices))
            #print(indices,minmax)
            #print(np.abs(np.abs(x[indices[ii+1]])-np.abs(x[indices[ii]])),min_transport,indices[ii],indices[ii+1])
            if np.abs(x[indices[ii+1]]-x[indices[ii]]) < min_transport:
                #print(np.abs(x[indices[ii+1]]-x[indices[ii]]),min_transport,indices[ii],indices[ii+1],x[indices[ii]],x[indices[ii+1]])
                if ii == 0: #if smin is involved and the transport is too small, smin has to change its min or max property
                    #print('if')
                    index.append(ii+1)
                    if minmax[ii] == 'min':
                        minmax[ii] = 'max'
                    else:
                        minmax[ii] = 'min'
                elif ii+1==len(indices)-1:#if smax is involved and the transport is too small, smin has to change its min or max property
                    #print('elif')
                    index.append(ii)
                    if minmax[ii+1] == 'min':
                        minmax[ii+1] = 'max'
                    else:
                        minmax[ii+1] = 'min'
                else: #else both involved div sals are kicked out
                    #print('else')
                    if ii+2 < len(indices)-1:
                    #check and compare to i+2
                        if minmax[ii]=='min':
                            if x[indices[ii+2]]>x[indices[ii]]:
                                index.append(ii+2)
                                index.append(ii+1)
                            else:
                                index.append(ii)
                                index.append(ii+1)
                        elif minmax[ii]=='max':
                            if x[indices[ii+2]]<x[indices[ii]]:
                                index.append(ii+2)
                                index.append(ii+1)
                            else:
                                index.append(ii)
                                index.append(ii+1)
                    else:
                        index.append(ii)
                        index.append(ii+1)
                #print(index)
                indices = np.delete(indices, index)
                minmax = np.delete(minmax, index)
                #print('after delete',indices,minmax)
            else:
                ii+=1
        
        ###
        #so far the first and last minmax does not correspond to smin and smax of the data, expecially smin due to numerical errors (only makes sense)
        #correct smin index
        ###
        
        #print(indices,minmax)
        if len(x)>4:
            ii=1
            while np.abs(np.abs(x[ii])-np.abs(x[0])) < 10**(-10) and ii < len(x)-1:
                ii+=1
            indices[0]=ii-1
            #correct smax index
            if x[-1]==0: #for low salinity classes Q[-1] might not be zero as supposed.
                jj=-1
                while x[jj] == 0 and np.abs(jj) < len(x)-1:
                    jj -=1
                indices[-1] = len(x)+jj+1
        return indices,minmax

def calc_bulk_values_new(coord,Qv,comp,min_trans='auto'):
    smin=coord[0]
    DeltaS=coord[1]-coord[0]
    if min_trans == 'auto':
        min_trans=0.01*np.max(np.abs(Qv))
    print('min_trans',min_trans)
    ind,minmax = find_extrema(Qv,min_trans)
    print(ind,minmax)
    div_sal=[]
    i=0
    while i < len(ind):
            #print(Qvl[ind[i]])
        div_sal.append(smin+DeltaS*ind[i])
        i+=1
            #print(smin+dss*ind[i])
        #calculate transports etc.
    Q_in_m=[]
    Q_out_m=[]
    index=[]
    i=0
    while i < len(ind)-1:
        Q_i=-(Qv[ind[i+1]]-Qv[ind[i]])
        if Q_i<0:
            Q_out_m.append(Q_i)
        elif Q_i > 0:
            Q_in_m.append(Q_i)
        else:
            index.append(i)
        i+=1
    div_sal = np.delete(div_sal, index)
    print(div_sal)
    print(Q_in_m)
    print(Q_out_m)
    return(Q_in_m,Q_out_m,div_sal,ind)

