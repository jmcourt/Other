#! /usr/bin/env python

import warnings

warnings.simplefilter("ignore")

import numpy as np
import pylab as pl
import matplotlib.gridspec as gridspec
import random

class density_chart():                                                    # The density_chart object

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
      self.xlims=[min(self.xvalues),max(self.xvalues)]                    # Extract the minimum and maximum values to plot between from the min and
                                                                          #  max values in the data.
      self.ylims=[min(self.yvalues),max(self.yvalues)]

      self.num_data=len(data[0])                                          # Fetch number of data points

      self.hist_res=0.05
      self.dens_res=0.02
      self.cmap='afmhot'
      self.has_dens=False

      self.x_diff=self.xlims[1]-self.xlims[0]
      self.y_diff=self.ylims[1]-self.ylims[0]
      self.x_range=np.arange(self.xlims[0],self.xlims[1]+self.dens_res*self.x_diff,self.dens_res*self.x_diff)
      self.y_range=np.arange(self.ylims[0],self.ylims[1]+self.dens_res*self.y_diff,self.dens_res*self.y_diff)

   def set_xlimit(self,xlim_lower,xlim_upper):
      self.xlims[0]=xlim_lower
      self.xlims[1]=xlim_upper
      self.x_diff=self.xlims[1]-self.xlims[0]
      self.x_range=np.arange(self.xlims[0],self.xlims[1]+self.dens_res*self.x_diff,self.dens_res*self.x_diff)

   def set_ylimit(self,ylim_lower,ylim_upper):
      self.ylims[0]=ylim_lower
      self.ylims[1]=ylim_upper
      self.y_diff=self.ylims[1]-self.ylims[0]
      self.y_range=np.arange(self.ylims[0],self.ylims[1]+self.dens_res*self.y_diff,self.dens_res*self.y_diff)

   def set_densitymap_resolution(self,density):
      self.dens_res=density
      self.x_range=np.arange(self.xlims[0],self.xlims[1]+self.dens_res*self.x_diff,self.dens_res*self.x_diff)
      self.y_range=np.arange(self.ylims[0],self.ylims[1]+self.dens_res*self.y_diff,self.dens_res*self.y_diff)

   def set_histogram_resolution(self,density):
      self.hist_res=density

   def plot(self):
      pixelwidth=int(1/self.dens_res)
      self.density_map=np.zeros([pixelwidth,pixelwidth])
      for datapoint in range(self.num_data):
         x,y=self.xvalues[datapoint],self.yvalues[datapoint]
         grid_x=int((x-self.xlims[0])*pixelwidth/self.x_diff)
         grid_y=int((y-self.ylims[0])*pixelwidth/self.y_diff)
         if grid_x>=0 and grid_x<pixelwidth and grid_y>=0 and grid_y<pixelwidth:
            self.density_map[grid_y,grid_x]+=1
      self.has_dens=True

   def show(self):
      if self.has_dens:
         f=pl.figure()
         gs=gridspec.GridSpec(2, 2, width_ratios=[3,1], height_ratios=[1,3])
         ax0=pl.subplot(gs[0])
         ax1=pl.subplot(gs[1])
         ax2=pl.subplot(gs[2])
         ax3=pl.subplot(gs[3])
         ax1.axis('off')
         ax0.hist(self.xvalues,bins=int(1/self.hist_res),range=(self.xlims[0],self.xlims[1]))
         ax0.get_xaxis().set_visible(False)
         ax0.get_yaxis().set_visible(False)
         ax0.get_yaxis().set_visible(False)
         ax0.set_xlim(self.xlims[0],self.xlims[1])
         ax3.hist(self.yvalues,bins=int(1/self.hist_res),range=(self.ylims[0],self.ylims[1]),orientation='horizontal')
         ax3.get_xaxis().set_visible(False)
         ax3.get_yaxis().set_visible(False)
         ax3.get_xaxis().set_visible(False)
         ax3.set_ylabel(self.ylabel)
         ax3.set_ylim(self.ylims[0],self.ylims[1])
         ax2.pcolor(self.x_range,self.y_range,self.density_map,cmap=self.cmap)
         ax2.set_xlabel(self.xlabel)
         ax2.set_ylabel(self.xlabel)
         ax2.set_ylim(self.ylims[0],self.ylims[1])
         ax2.set_xlim(self.xlims[0],self.xlims[1])
         f.subplots_adjust(hspace=0)
         f.subplots_adjust(wspace=0)
         pl.show(block=False)
      
      
