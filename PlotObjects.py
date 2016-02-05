#! /usr/bin/env python

import warnings

warnings.simplefilter("ignore")

import scipy.stats as st
import numpy as np
import pylab as pl
import matplotlib.gridspec as gridspec
import random
import matplotlib.patches as mpatches
import imp

pan = imp.load_source('pan_lib.py', '/home/jamie/Documents/Data/Data_Management/PANTHEON/pan_lib.py')
      

class chart():

   # Need PLOT function, which sets up the data for the plot, and a MAKE_PLOT function which prepares the actual plot itself

   def plot(self):
      pass

   def make_plot(self):
      pass

   def startup(self):                                                     # ===Plot environment initialiser===
      self.xlabel=''
      self.ylabel=''
      self.zlabel=''
      self.is_plotted=False
      self.xlims=[0,1]
      self.ylims=[0,1]
      self.colormap='cool'                                                # Fetch name of colormap (so it can be changed by user if needs be)
                        
   def set_xlabel(self,xlabel):                                           # ===Setter for xlabel===
      self.xlabel=xlabel

   def set_ylabel(self,ylabel):                                           # ===Setter for ylabel===
      self.ylabel=ylabel

   def set_zlabel(self,zlabel):                                           # ===Setter for zlabel===
      self.zlabel=zlabel

   def set_colormap(self,colormap):                                       # ===Set colormap for the densitymap===
      self.colormap=colormap

   def show(self):                                                        # ===Display the plot===
      if self.is_plotted:
         self.make_plot()
      else:
         self.plot()
         self.make_plot()
      self.fig.show()

   def save(self,savename):                                               # ===Display the plot===
      if self.is_plotted:
         self.make_plot()
      else:
         self.plot()
         self.make_plot()
      self.fig.savefig(savename)




class density_chart(chart):                                               # ===The density_chart object===

   '''Density Chart.

   Available actions:

    chart.set_densitymap_resolution(x)
    chart.set_histogram_resolution(x)
    chart.set_colormap(x)
    chart.set_xlimit(x,y)
    chart.set_ylimit(x,y)
    chart.set_xlabel(x)
    chart.set_ylabel(x)
    chart.show_pearson()
    chart.hide_pearson()
    chart.plot()
    chart.show()
    chart.save()

   '''

   def __init__(self,data):                                               # Must provide two dimensional data to the object.  This can consist of a
                                                                          #  tuple containing the list of x-values in element zero and the identical
                                                                          #  length list of y-values in element one.

      self.startup()                                                      # Basic initialisation
      if len(data)!=2:
         data=np.array(data).transpose()                                  # Allow ill-formatted data to be transposed to see if the transpose can be
                                                                          #  interpreted as two equal-length data series.
      assert len(data)==2                                                 # Crash if data is ill-formatted

      self.xvalues=data[0]                                                # Extract x-values
      self.yvalues=data[1]                                                # Extract y-values
      self.dens_res=1                                                     # Set up dummy variables to be filled later
      self.hist_res=1
      self.num_data=len(data[0])                                          # Fetch number of data points

      assert len(data[0])==len(data[1])

      self.set_xlimit(min(self.xvalues),max(self.xvalues))                # Set the limits to a default value (the max and min values on each axis)
      self.set_ylimit(min(self.yvalues),max(self.yvalues))
      self.set_densitymap_resolution(0.01)                                # Set the densitymap resolution to a default value
      self.set_histogram_resolution(0.02)                                 # Set the histogram resolution to a default value
      self.plot_pearson=False                                             # Don't show Pearson Coefficient by default

   def set_densitymap_resolution(self,density):                           # ===Set the densitymap resolution===
      self.dens_res=density                                               #    Densitymap resolution = the input value
      self.make_ranges('xy')                                              #    Recalculate x and y axis values

   def set_histogram_resolution(self,density):                            # ===Set the histogram resolution===
      self.hist_res=density                                               #    Histogram resolution = the input value

   def set_xlimit(self,xlim_lower,xlim_upper):                            # ===Set the limits on the x-axis===
      self.xlims[0]=xlim_lower                                            #    Fetch lower limit
      self.xlims[1]=xlim_upper                                            #    Fetch upper limit
      self.x_diff=self.xlims[1]-self.xlims[0]                             #    Store difference between limits
      self.make_ranges('x')                                               #    Re-Create x range.

   def set_ylimit(self,ylim_lower,ylim_upper):                            # ===Set the limits on the x-axis===
      self.ylims[0]=ylim_lower                                            #    Fetch lower limit
      self.ylims[1]=ylim_upper                                            #    Fetch upper limit
      self.y_diff=self.ylims[1]-self.ylims[0]                             #    Store difference between limits
      self.make_ranges('y')                                               #    Re-Create y range.     

   def show_pearson(self):                                                #    Display Pearson Coefficient in the final plot
      self.plot_pearson=True

   def hide_pearson(self):                                                #    Hide Pearson Coefficient in the final plot
      self.plot_pearson=False

   def make_ranges(self,xy='xy'):                                         # ===Make ranges of x and y axis values===
      if 'x' in xy:                                                       #    Allow selective making of only one range
         self.x_range=np.arange(self.xlims[0],self.xlims[1]+0.1*self.dens_res*self.x_diff,self.dens_res*self.x_diff)
      if 'y' in xy:
         self.y_range=np.arange(self.ylims[0],self.ylims[1]+0.1*self.dens_res*self.y_diff,self.dens_res*self.y_diff)

      # The term 0.1*self.dens_res*self.x_diff forces the range to extend to the upper value, while the 0.1 prevents it going any further
      # which it tends to do, presumably due to floating point error. 

   def plot(self):                                                        # ===Prepare Plot Data===
      pixelwidth=int(len(self.x_range))                                   #    Fetch the width, in pixels, of the densitymap
      self.density_map=np.zeros([pixelwidth,pixelwidth])                  #    Create blank densitymap
      for datapoint in range(self.num_data):                              #    For each x,y pair in the data...
         x,y=self.xvalues[datapoint],self.yvalues[datapoint]
         grid_x=int((x-self.xlims[0])*pixelwidth/self.x_diff)             #    Fetch the corresponding pixel that corresponds with the datapoint
         grid_y=int((y-self.ylims[0])*pixelwidth/self.y_diff)
         if grid_x>=0 and grid_x<pixelwidth and grid_y>=0 and grid_y<pixelwidth:
            self.density_map[grid_y,grid_x]+=1                            #    If pixel is valid, add one to its value
      self.is_plotted=True                                                #    Let the object know its ready to display

   def make_plot(self):                                                   # ===Display/Save Plot===
      self.fig=pl.figure()                                                #    Create the figure and the grid, noting size ratios of the panels
      gs=gridspec.GridSpec(2, 2, width_ratios=[3,1], height_ratios=[1,3])
      ax0=pl.subplot(gs[0])                                               #    Assign IDs to the cells in the grid
      ax1=pl.subplot(gs[1])
      ax2=pl.subplot(gs[2])
      ax3=pl.subplot(gs[3])
      ax0.hist(self.xvalues,bins=int(1/self.hist_res),range=(self.xlims[0],self.xlims[1])) # Plot the x-axis histogram
      ax0.get_xaxis().set_visible(False)                                  #    Hide both axes on this panel
      ax0.get_yaxis().set_visible(False)
      ax0.set_xlim(self.xlims[0],self.xlims[1])                           #    Set the plot limits
      ax1.axis('off')                                                     #    Hide the top-left panel
      if self.plot_pearson:                                               #    If requested, print the Pearson Correlation Coefficient in the empty panel
         ax1.text(0.1,0.01,'Pearson Coeff. ='+str(st.pearsonr(self.xvalues,self.yvalues)[0])[:4])
      ax2.pcolor(self.x_range,self.y_range,self.density_map,cmap=self.colormap) # Plot the densitymap
      ax2.set_xlabel(self.xlabel)                                         #    Place labels
      ax2.set_ylabel(self.ylabel)
      ax2.set_ylim(self.ylims[0],self.ylims[1])                           #    Set both limits for this panel
      ax2.set_xlim(self.xlims[0],self.xlims[1])
      ax3.hist(self.yvalues,bins=int(1/self.hist_res),range=(self.ylims[0],self.ylims[1]),orientation='horizontal') # Plot the y-axis histogram
      ax3.get_xaxis().set_visible(False)                                  #    Hide both axes on this panel
      ax3.get_yaxis().set_visible(False)
      ax3.set_ylim(self.ylims[0],self.ylims[1])                           #    Set the plot limits 
      self.fig.subplots_adjust(hspace=0)                                  #    Remove the whitespace between panels
      self.fig.subplots_adjust(wspace=0)




class lightcurve_ls(chart):                                               # ===The Lightcurve_LS object===

   '''Lightcurve/LombScargle Chart.

   Available actions:

    chart.set_window_size(x)
    chart.set_timestep(x)
    chart.set_freqstep(x)
    chart.set_flimit(x,y)
    chart.set_colormap(x)
    chart.set_xlabel(x)
    chart.set_ylabel(x)
    chart.set_ylabel2(x)
    chart.set_zlabel(x)
    chart.plot()
    chart.show()
    chart.show_Inu(lag=0)
    chart.save()

   '''

   def __init__(self,times,counts,errors):                                #    Must provide 3  1-dimensional datasets to the object, corresponding to times,
                                                                          #     values and errors.

      self.startup()                                                      #    Basic initialisation

      self.freq_stp_size=0.001                                            #    Setup frequency stepsize
      self.freq_low_lim=0.01                                              #    Setup frequency lower limit
      self.freq_upp_lim=0.4                                               #    Setup frequency upper limit
      self.make_freq_array()                                              #    Setup frequency range

      self.ylabel2=''

      self.times=np.array(times)                                          #    Save data
      self.counts=np.array(counts)
      self.errors=np.array(errors)

      self.time_binning=self.times[1]-self.times[0]                       #    Fetch the data binning

      self.win_size=int(31.25/self.time_binning)                          #    Default 31.25s windows
      self.time_stp_size=int(1.25/self.time_binning)                      #    Default 1.25s slide between windows

      self.plot_maxfreqs=False

   def make_freq_array(self):                                             # ===Construct frequency array===
      self.freqs=np.arange(self.freq_low_lim,self.freq_upp_lim,self.freq_stp_size)

   def show_max_freqs(self):                                              # ===Add a plot of max frequencies to object===
      self.plot_maxfreqs=True

   def hide_max_freqs(self):                                              # ===Remove plot of max frequencies from object===
      self.plot_maxfreqs=False

   def set_ylabel2(self,ylabel2):                                         # ===Setter for ylabel2===
      self.ylabel2=ylabel2

   def set_window_size(self,window_size):                                 # ===Setter for sliding window size in seconds===
      self.win_size=int(window_size/self.time_binning)

   def set_timestep(self,timestep):                                       # ===Setter for time stepsize===
      self.time_stp_size=int(timestep/self.time_binning)

   def set_freqstep(self,freqstep):                                       # ===Setter for frequency step size===
      self.freq_stp_size=freqstep
      self.make_freq_array()                                              #    Reconstruct the frequency array

   def set_freqlimit(self,f_low,f_high):                                  # ===Setter for upper and lower frequency limits===
      self.freq_low_lim=f_low                                             #    Set lower frequency limit
      self.freq_upp_lim=f_high                                            #    Set upper frequency limit
      self.make_freq_array()                                              #    Reconstruct the frequency array

   def plot(self):                                                        # ===Prepare Plot Data===
      spectrogram=[]                                                      #    Setup blank list to append spectra into
      lcurve=[]                                                           #    Setup blank list to append mean values into
      maxfreqs=[]
      prog=None                                                           #    Token needed to print % completion to screen
      for i in range(len(self.times)-self.win_size)[::self.time_stp_size]:
         prog2=(i*10)/(len(self.times)-self.win_size)
         if prog2!=prog:
            print 'Plotting:',prog2*10,'%'                                #    Print % complete every 10%
            prog=prog2
         spectrum=pan.lomb_scargle(self.times[i:i+self.win_size],self.counts[i:i+self.win_size],self.errors[i:i+self.win_size],self.freqs)
         spectrogram.append(spectrum)
         maxfreqs.append(self.freqs[np.argmax(spectrum)])
         lcurve.append(np.mean(self.counts[i:i+self.win_size]))           #    Append spectrum and average value
      self.spectrogram=(np.array(spectrogram)/1000.0).transpose()         #    Transpose spectrum/time matrix
      self.lcurve=np.array(lcurve)
      self.maxfreqs=np.array(maxfreqs)
      self.taxis=self.times[:(len(self.times)-self.win_size)][::self.time_stp_size] # Setup the time axis
      self.is_plotted=True                                                #    Let object know it is plotted

   def make_plot(self):                                                   # ===Display/Save Plots===
      self.fig=pl.figure()                                                #    Create the figure object
      ax1=self.fig.add_axes([0.1,0.1,0.65,0.8])                           #    Create the spectrogram axes
      pc=ax1.pcolor(self.taxis,self.freqs,self.spectrogram,cmap=self.colormap) #    Plot spectrogram
      ax1.set_xlabel(self.xlabel)                                         #    Set global x-label
      ax1.set_ylim(self.freqs[0],self.freqs[-1])                          #    Set y-limits of spectrogram
      ax1.set_ylabel(self.ylabel)                                         #    Set y-label of spectrogram
      position=self.fig.add_axes([0.85,0.1,0.03,0.8])                     #    Setup position of colorbar
      cbar=self.fig.colorbar(pc,cax=position)                             #    Make colorbar
      cbar.set_label(self.zlabel+' (*1000)', rotation=270,labelpad=15)    #    Set z-label
      ax2 = ax1.twinx()                                                   #    Create the lightcurve axes
      ax2.yaxis.tick_right()                                              #    Force the lightcurve y-axis to the right
      ax2.yaxis.set_label_position('right')                               #    Push the label over there too
      ax2.plot(self.taxis,self.lcurve,'k')                                #    Plot the lightcurve
      ax2.set_ylim(0,max(self.lcurve)*1.1)                                #    Set y-limits of lightcurve
      ax2.set_xlim(self.taxis[0],self.taxis[-1])                                    #    Set global x-limits
      ax2.set_ylabel(self.ylabel2,rotation=-90,labelpad=15)               #    Set y-label of lightcurve
      black_patch = mpatches.Patch(color='black', label='Count Rate')     #    Create object to represent the lightcurve in the key
      if self.plot_maxfreqs==True:
         ax2.plot(self.taxis,((self.maxfreqs-self.freqs[0])*max(self.lcurve)*1.1/self.freqs[-1]))
         blue_patch = mpatches.Patch(color='blue', label='Peak Frequency')#    Create object to represent the lightcurve in the key
         pl.legend(handles=[black_patch,blue_patch])                      #    Create the key
      else:
         pl.legend(handles=[black_patch])

   def show_Inu(self,lag=0):                                              #    Feature to quickly construct a 2D histogram of peak frequency against intensity
      if not self.is_plotted:
         self.plot()
      if lag=='auto':                                                     #    Lag offsets the two datasets against each other by a time t.  If 'auto', this time t is
                                                                          #       the sliding window size.
         lag=self.win_size*self.time_binning
      c_lag=int(lag/(self.time_binning*self.time_stp_size))
      if c_lag==0:
         x=self.lcurve
         y=self.maxfreqs
         textra=''
      elif lag>0:
         x=self.lcurve[c_lag:]
         y=self.maxfreqs[:-c_lag]
         textra=' ('+str(lag)+'s lag)'
      else:
         x=self.lcurve[:c_lag]
         y=self.maxfreqs[-c_lag:]
         textra=' ('+str(lag)+'s lag)'
         
      den_chart=density_chart([x,y])
      den_chart.set_xlabel(r'Intensity (cts s$^{-1}$)')
      den_chart.set_ylabel('Peak Frequency (Hz)'+textra)
      den_chart.show_pearson()
      den_chart.set_colormap('inferno')
      den_chart.plot()
      den_chart.show()

      
