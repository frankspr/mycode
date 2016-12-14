#!/usr/bin/env python
import os,sys
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
sys.path.append(basepath)
from model import codepush 
if __name__ == '__main__':
  c = codepush.pushcode()
  c.pushjob(environ='test',appname='website',version='website_201611281433')
#  c.rollbackapp(environ='test',appname='website',version='website_201611291417')
#  c.pushjob(environ='pre',appname='website',version='website_201611281433')
#  c.rollbackapp(environ='pre',appname='website',version='website_201611291417')
#  c.pushjob(environ='prod',appname='website',version='website_201611281433')
#  c.rollbackapp(environ='prod',appname='website',version='website_201611291417')
