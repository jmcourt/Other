#! /usr/bin/env python

import warnings

warnings.simplefilter("ignore")

import numpy as np
import pylab as pl
import matplotlib.gridspec as gridspec
import random

class density_chart():                                                    # ===The density_chart object===

   '''Density Chart.

   Available actions:

    chart.set_densitymap_resolution()
    chart.set_histogram_resolution()
    chart.set_colormap()
    chart.set_xlimit()
    chart.set_ylimit()
    chart.plot()
    chart.show()

   '''

   def __init__(self,data):                                               # Must provide two dimensional data to the object.  This can consist of a
                                                                          #  tuple containing the list of x-values in element zero and the identical
                                                                          #  length list of y-values in element one.
      if len(data)!=2:
         data=np.array(data).transpose()                                  # Allow ill-formatted data to be transposed to see if the transpose can be
                                                                          #  interpreted as two equal-length data series.
      assert len(data)==2                                                 # Crash if data is ill-formatted
      self.xvalues=data[0]                                                # Extract x-values
      self.yvalues=data[1]                                                # Extract y-values
      self.xlabel=''                                                      # Set default x-label as blank (to be changed by user)
      self.ylabel=''                                                      # Set default y-label as blank (to be changed by user)

      self.xlims=[0,0]                                                    # Set up dummy variables to be filled later
      self.ylims=[0,0]
      self.dens_res=1
      self.hist_res=1

      self.num_data=len(data[0])                                          # Fetch number of data points

      self.set_colormap('afmhot')                                         # Fetch name of colormap (so it can be changed by user if needs be)
      self.has_dens=False                                                 # Tell the code it has not plotted the density map yet

      self.set_xlimit(min(self.xvalues),max(self.xvalues))                # Set the limits to a default value (the max and min values on each axis)
      self.set_ylimit(min(self.yvalues),max(self.yvalues))

      self.set_densitymap_resolution(0.01)                                # Set the densitymap resolution to a default value
      self.set_histogram_resolution(0.02)                                 # Set the histogram resolution to a default value

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

   def make_ranges(self,xy='xy'):                                         # ===Make ranges of x and y axis values===
      if 'x' in xy:                                                       #    Allow selective making of only one range
         self.x_range=np.arange(self.xlims[0],self.xlims[1]+0.1*self.dens_res*self.x_diff,self.dens_res*self.x_diff)
      if 'y' in xy:
         self.y_range=np.arange(self.ylims[0],self.ylims[1]+0.1*self.dens_res*self.y_diff,self.dens_res*self.y_diff)

      # The term 0.1*self.dens_res*self.x_diff forces the range to extend to the upper value, while the 0.1 prevents it going any further
      # which it tends to do, presumably due to floating point error. 

   def set_colormap(self,colormap):                                       # ===Set colormap for the densitymap===
      self.cmap=colormap                                                  #    Colormap=input

   def plot(self):                                                        # ===Prepare Plot===
      pixelwidth=int(len(self.x_range))                                   #    Fetch the width, in pixels, of the densitymap
      self.density_map=np.zeros([pixelwidth,pixelwidth])                  #    Create blank densitymap
      for datapoint in range(self.num_data):                              #    For each x,y pair in the data...
         x,y=self.xvalues[datapoint],self.yvalues[datapoint]
         grid_x=int((x-self.xlims[0])*pixelwidth/self.x_diff)             #    Fetch the corresponding pixel that corresponds with the datapoint
         grid_y=int((y-self.ylims[0])*pixelwidth/self.y_diff)
         if grid_x>=0 and grid_x<pixelwidth and grid_y>=0 and grid_y<pixelwidth:
            self.density_map[grid_y,grid_x]+=1                            #    If pixel is valid, add one to its value
      self.has_dens=True                                                  #    Let the object know its ready to display

   def show(self):                                                        # ===Display Plot===
      if self.has_dens:                                                   #    If object believes it is ready to plot...
         f=pl.figure()                                                    #    Create the figure and the grid, noting size ratios of the panels
         gs=gridspec.GridSpec(2, 2, width_ratios=[3,1], height_ratios=[1,3])
         ax0=pl.subplot(gs[0])                                            #    Assign IDs to the cells in the grid
         ax1=pl.subplot(gs[1])
         ax2=pl.subplot(gs[2])
         ax3=pl.subplot(gs[3])
         ax0.hist(self.xvalues,bins=int(1/self.hist_res),range=(self.xlims[0],self.xlims[1])) # Plot the x-axis histogram
         ax0.get_xaxis().set_visible(False)                               #    Hide both axes on this panel
         ax0.get_yaxis().set_visible(False)
         ax0.set_xlim(self.xlims[0],self.xlims[1])                        #    Set the plot limits
         ax1.axis('off')                                                  #    Hide the top-left panel
         ax2.pcolor(self.x_range,self.y_range,self.density_map,cmap=self.cmap) # Plot the densitymap
         ax2.set_xlabel(self.xlabel)                                      #    Place labels
         ax2.set_ylabel(self.xlabel)
         ax2.set_ylim(self.ylims[0],self.ylims[1])                        #    Set both limits for this panel
         ax2.set_xlim(self.xlims[0],self.xlims[1])
         ax3.hist(self.yvalues,bins=int(1/self.hist_res),range=(self.ylims[0],self.ylims[1]),orientation='horizontal') # Plot the y-axis histogram
         ax3.get_xaxis().set_visible(False)                               #    Hide both axes on this panel
         ax3.get_yaxis().set_visible(False)
         ax3.set_ylim(self.ylims[0],self.ylims[1])                        #    Set the plot limits
         f.subplots_adjust(hspace=0)                                      #    Remove the whitespace between panels
         f.subplots_adjust(wspace=0)
         pl.show(block=False)                                             #    Show the plot!
      else:
         self.plot()                                                      #    If it hasn't been plotted already, plot it now
         self.show()                                                      #    Try this again
      
      
