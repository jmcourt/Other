#! /usr/bin/env python

import warnings

warnings.simplefilter("ignore")

import numpy as np
import pylab as pl

class statrange():

   def __init__(self,data):
      data.sort()
      self.data=data
      self.len=len(data)
      self.is_llim=False
      self.is_ulim=False

   def low(self,pct):
      pct=int(pct*self.len/100.0)
      self.is_llim=True
      self.llim=self.data[pct]
      return self.data[pct]

   def high(self,pct):
      pct=int(((100.0-pct)*self.len)/100.0)
      self.is_ulim=True
      self.ulim=self.data[pct]
      return self.data[pct]

   def range(self,low_pct,high_pct):
      return self.low(low_pct),self.high(high_pct)

   def eqrange(self,pct):
      return self.range(pct,pct)

   def plot(self):
      pl.close()
      pl.figure()
      h=max(pl.hist(np.array(self.data),bins=100,color='0.5',linewidth=0)[0])
      print h
      if self.is_ulim:
         pl.plot([self.ulim,self.ulim],[0,h*1.1],'b')
      if self.is_llim:
         pl.plot([self.llim,self.llim],[0,h*1.1],'r')
      pl.ylim(0,h*1.1)
      pl.show()
