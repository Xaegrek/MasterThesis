from include import globalVariables as gVar

from scipy import interpolate as intp
from scipy import linspace

from dronekit import *
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys


def vehicleStay():
	time.sleep(gVar.flyTime)

def vehicleMoveVelocity():
	return

def vehicleMoveDistance(pathPoint,speed):
	gVar.UAVS.simple_goto(pathPoint,speed)
	while gVar.UAVS.locations.local_frame != pathPoint:
		gVar.posHistory.append([gVar.UAVS.locations.local_frame])
		time.sleep(0.2)
	return

def simpleArcInterpolater(path):
	# takes:
	# 	current gps position
	# goal:
	# 	path and iterplotae set of GPS cooridanets
	num_true_pts = 50
	pathD = [[],[],[]]
	smoothPath = []
	for i in range(len(path)):
		pathD[0].append(path[i][0])
		pathD[1].append(path[i][1])
		pathD[2].append(path[i][2])
	tck, u = intp.splprep(pathD)
	u_fine = linspace(0, 1, num_true_pts)
	x_fine, y_fine, z_fine = intp.splev(u_fine, tck)
	for i in range(len(x_fine)):
		smoothPath.append([x_fine[i], y_fine[i], z_fine[i]])
	return smoothPath

def pathFollow(path):
	gVar.coordinatesGPS = gVar.UAVS.locations.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.locations.local_frame
	for i in range(len(path)):
		vehicleMoveDistance(path[i],gVar.uSpeed)
	return