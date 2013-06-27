#==========#==========#==========#==========#==========#==========#==========#=========
# process all images in current directory so they can be shown in my awesome d3 picture
# showing framework

import glob
import Image
import random
import os
import math
import copy
import pdb
import argparse
import json


def scatter(points, strength, iterations):
	""" scatter points by moving each point away from its nearest neighbour 
	points should be of format [(x,y),(x,y)]"""
	
	for i in range(iterations):
		points = [pushclosest(p,points,strength) for p in points]
		    
	return points


def pushclosest(a,points,strength):
	"""push the point closest to point a and push it away
		"""
	c = closest(points,a)
	
	direction = normvector(a,c)
	if direction == (0,0):
		direction = randomizevector(direction,1)
		
	distance = dist(a,c)
	if distance == 0:
		distance = 0.01
		
	if distance > 140:
		distance = 1000
		
	f = strength * math.log(1+(1/distance))
	pushed = addvector(a,multvector(direction,f))
	
	
	return pushed
	

def randomizevector(a,f):
	return (a[0]+random.randint(-f,f),a[1]+random.randint(-f,f))

def multvector(a,f):
	return (a[0]*f,a[1]*f)

def addvector(a,b):
	return (a[0]+b[0],a[1]+b[1])

def normvector(a,b):
	"""I dont want to install extra libs. Just code this again. Norm vector for 2d point a and b"""
	diff = (a[0]-b[0], a[1]-b[1])
	if diff == (0,0):
		return (0,0)
	else:
		d = dist(a,b)
		return (diff[0]/d,diff[1]/d)


def closest(points,a):
	"""return point closest to point a which is not a"""	
	s = sorted(zip(points,distances(points,a)),key=lambda x: x[1])
	return s[1][0]
	

def distances(points,a):
	return [dist(a,i) for i in points]

def dist(a,b):
	"""2d euclidian distance """
	if a == b:
		return 0
	else:
		return math.hypot(a[0]-b[0], a[1]-b[1])
    
def log(m,level=""):
	if level == "warn":
		m = "Warning - " + m
	if level == "error":
		m = "Error - " + m	
	print "* "+m


def process(dir):

	startdir = os.getcwd()
	os.chdir(dir)
	
	log("processing dir '%s'" % dir)
	log("creating thumbnails")
	#create thumbnails of each image
	files = []
	# get all the jpg files from the current folder, and save copy as thumbnails
	for infile in glob.glob("*.jpg"):
		im = Image.open(infile)
		# don't save if thumbnail already exists
		if infile[0:2] != "T_":
			# convert to thumbnail image
			im.thumbnail((128, 128), Image.ANTIALIAS)
			# prefix thumbnail file with T_
			thumbfile = "T_" + infile
			files.append(infile)
			im.save(thumbfile,"JPEG")


	# create a list of locations and thumbnail names
	left = 100 #start random sampling here
	top = 100 
	w = 600
	h = 400

	# try to get them on a grid randomly but not totally overlapping
	# hobby project method: sample randomly on coarse grid

	# approximate number of gridpoints in height and width
	n = int(math.ceil(math.sqrt(len(files))))  # assume square space, if not
											   # square grid will be squashed
	n = n*2 # make sure there is room for randomness

	# create course gridpoints
	#gridpoints = []
	#for x in range(n):
	#	for y in range(n):
	#		gridpoints.append(((x+1)*(w/n)+left,(y+1)*(h/n)+top))
	
	log("generating thumbnail positions")
	
	gridpoints = [(300,300) for i in range(len(files))]


	# sample random points
	#gridpoints = [gridpoints[i] for i in random.sample(range(len(gridpoints)),len(files))]
	gridpoints = scatter(gridpoints,20,400)

	currentdir =  os.path.basename(os.getcwd())

	log("writing positions to %s/files.csv"%currentdir)
	f = open("files.csv",'w')
	f.write("x,y,filename,thumb\n")
	i = 0
	for infile,gridpoint in zip(files,gridpoints):
		f.write("%s,%s,%s,%s\n" % (str(gridpoint[0]),
								str(gridpoint[1]),
								infile,
								"T_"+infile)
				)
		i += 1;
	f.close()
	os.chdir(startdir)
	log("done")
	
	
def getsubfolders(folder):
	return [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

# =========================== main execution =============================

parser = argparse.ArgumentParser(description='Process folder of jpg images for use\
											  in Sjoerd website structure')
parser.add_argument('folders', metavar='N', nargs='+',
                   help='names of folders to process')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')

args = parser.parse_args()

menufile = "menu.js"

	
#will hold all menu items to write to file
menu = []



imagebasefolder = args.folders[0]
subfolders = getsubfolders(imagebasefolder)


for foldername in subfolders:
	folder = imagebasefolder+"/"+foldername
	if not folder.startswith("./"):
		folder = "./"+folder
	#check if folder exists
	if not os.path.exists(folder):
		log("folder %s does not exist, skipping." %folder,"warn")
		continue
	else:
		try:
			process(folder)
		except Exception as e:
			log("Error while processing %s :'%s'. Continuing with next \
				folder.." %(folder,str(e)),"error")
			continue
		menu.append({"dir":folder+"/","name":os.path.basename(os.path.normpath(folder))})

			
try:
	f = open(menufile,"w")
except Exception as e:
	log("error opening menufile '%s': \
		'%s'." % (menufile,str(e)),'error')

#write a jquery array which is included in the site to render petals.
f.write("var dirs = " + json.dumps(menu))


