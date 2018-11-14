#!/usr/bin/env python
# coding=UTF-8

import os

BASEPATH = os.path.dirname(os.path.abspath(__file__))

#########################################
# Server setting                        #
#########################################
HOST = os.environ['HOST']
PORT = int(os.environ['PORT'])

SECRET_KEY = os.environ['SECRET_KEY']
#########################################


#########################################
# Database setting                      #
#########################################
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
#########################################


#########################################
# Logging settings                      #
#########################################
LOG_LEVEL = os.environ['LOG_LEVEL'].upper()
#########################################
