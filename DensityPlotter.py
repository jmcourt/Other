#! /usr/bin/env python

import warnings

warnings.simplefilter("ignore")

import numpy as np
import pylab as pl
import matplotlib.gridspec as gridspec
import random

class density_chart():

   def __init__(self,data):
      if len(data)!=2:
         data=np.array(data).transpose()
      assert len(data)==2
      self.xvalues=data[0]
      self.yvalues=data[1]
      self.xlabel=''
      self.ylabel=''
      self.xlims=[min(self.xvalues),max(self.xvalues)]
      self.ylims=[min(self.yvalues),max(self.yvalues)]

      if self.xlims[0]<0:
         self.xlims[0]=0
      if self.ylims[0]<0:
         self.ylims[0]=0

      self.num_data=len(data[0])

      self.hist_res=0.05
      self.dens_res=0.01
      self.cmap='afmhot'
      self.has_dens=False

      self.x_diff=self.xlims[1]-self.xlims[0]
      self.y_diff=self.ylims[1]-self.ylims[0]
      self.x_range=np.arange(self.xlims[0],self.xlims[1]+self.dens_res*self.x_diff,self.dens_res*self.x_diff)
      self.y_range=np.arange(self.ylims[0],self.ylims[1]+self.dens_res*self.y_diff,self.dens_res*self.y_diff)

   def set_densitymap_resolution(self,density):
      self.dens_res=density
      self.x_range=np.arange(self.xlims[0],self.xlims[1]+self.dens_res*self.x_diff,self.dens_res*self.x_diff)
      self.y_range=np.arange(self.ylims[0],self.ylims[1]+self.dens_res*self.y_diff,self.dens_res*self.y_diff)

   def set_histogram_resolution(self,density):
      self.hist_res=density

   def make_densitymap(self):
      pixelwidth=int(1/self.dens_res)+1
      self.density_map=np.zeros([pixelwidth,pixelwidth])
      for datapoint in range(self.num_data):
         x,y=self.xvalues[datapoint],self.yvalues[datapoint]
         grid_x=int((x-self.xlims[0])*pixelwidth/self.xlims[1])
         grid_y=int((y-self.ylims[0])*pixelwidth/self.ylims[1])
         if grid_x>=0 and grid_x<pixelwidth and grid_y>=0 and grid_y<pixelwidth:
            self.density_map[grid_y,grid_x]+=1
      self.has_dens=True

   def plot_diagram(self):
      if self.has_dens:
         f=pl.figure()
         gs=gridspec.GridSpec(2, 2, width_ratios=[1,3], height_ratios=[3,1])
         ax0=pl.subplot(gs[0])
         ax1=pl.subplot(gs[1])
         ax2=pl.subplot(gs[2])
         ax3=pl.subplot(gs[3])
         ax0.hist(self.yvalues,bins=int(1/self.hist_res),range=(self.ylims[0],self.ylims[1]),orientation='horizontal')
         ax0.invert_xaxis()
         ax0.get_xaxis().set_visible(False)
         ax0.set_ylabel(self.ylabel)
         ax0.set_ylim(self.ylims[0],self.ylims[1])
         ax1.pcolor(self.x_range,self.y_range,self.density_map,cmap=self.cmap)
         ax1.get_xaxis().set_visible(False)
         ax1.get_yaxis().set_visible(False)
         ax1.set_ylim(self.ylims[0],self.ylims[1])
         ax1.set_xlim(self.xlims[0],self.xlims[1])
         ax2.axis('off')
         ax3.hist(self.xvalues,bins=int(1/self.hist_res),range=(self.xlims[0],self.xlims[1]))
         ax3.invert_yaxis()
         ax3.set_xlabel(self.xlabel)
         ax3.get_yaxis().set_visible(False)
         ax3.set_xlim(self.xlims[0],self.xlims[1])
         f.subplots_adjust(hspace=0)
         f.subplots_adjust(wspace=0)
         pl.show(block=False)
      
      
