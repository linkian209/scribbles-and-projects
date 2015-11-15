# Genetic Programming
# ---------------------------
# Creates squares from random
# points over generations.
# Author: Ian Drake Copyright: 2015

import matplotlib.pyplot as plt
import sys, numpy
from random import randint, random

def distance(Coord1,Coord2):
	retval = numpy.sqrt(numpy.absolute(numpy.power(Coord2.x - Coord1.x,2) + numpy.power(Coord2.y - Coord1.y,2)))
	return retval

# Coordinate class
class Coord:
	def __init__(self,x,y,options):
		self.x = x
		self.y = y
		self.options = options
		
def individual(min,max):
	retval = []
	temp = []
	temp.append(Coord(randint(min,max),randint(min,max),'bo'))
	while( len(temp) < 4 ):
		exists = True
		while exists:
			x = randint(min,max)
			y = randint(min,max)
			for b in range(len(temp)):
				if(x == temp[b].x and y == temp[b].y):
					exists = True
					break
				else:
					exists = False
			if(not(exists)):
				temp.append(Coord(x,y,'bo'))
	retval = temp
	return retval
	
def population(count,min,max):
	return [ individual(min,max) for x in range(count) ]
	
def fitness(individual):
	costOfBecomingSkyNet = 99999999999
	
	isSquare = 0
	score = 0
	sides = []
	sides.append(distance(individual[0],individual[1]))
	sides.append(distance(individual[0],individual[2]))
	sides.append(distance(individual[0],individual[3]))
	
	equalSide1 = -1
	equalSide2 = -1
	unequalSide = -1
	
	if( sides[0] == sides[1] ):
		if( sides[0] != sides[2] ):
			equalSide1 = 0
			equalSide2 = 1
			unequalSide = 2
			score = score + .25
		score = score + 1 # two equal sides
	elif( sides[1] == sides[2] ):
		if( sides[1] != sides[0] ):
			equalSide1 = 1
			equalSide2 = 2
			unequalSide = 0
			score = score + .25
		score = score + 1 
	elif( sides[0] == sides[2] ):
		if( sides[0] != sides[1] ):
			equalSide1 = 0
			equalSide2 = 2
			unequalSide = 1
			score = score + .25
		score = score + 1
	
	# Check to see if can continue
	if( equalSide1 != -1 ):
		opposing = 0
		if( unequalSide == 0 ):
			opposing = distance(individual[2],individual[3])
		elif( unequalSide == 1 ):
			opposing = distance(individual[1],individual[3])
		elif( unequalSide == 2 ):
			opposing = distance(individual[1],individual[2])
		else:
			opposing == -1
			score = score - .75
		
		if( opposing == sides[unequalSide] ):
			score = score + 2 # equal diagonals
			diagonal = sides[unequalSide]
			adjacent = sides[equalSide1]
			stillOk = 1
			for a in range(0,4):
				diagonalCount = 0
				adjacentCount = 0
				for b in range(0,4):
					dist = distance(individual[a],individual[b])
					if( dist == diagonal ):
						diagonalCount = diagonalCount + 1
					elif( dist == adjacent ):
						adjacentCount = adjacentCount + 1
				# 1 diagonal and 2 adjacent sides?
				if( not(diagonalCount == 1 and adjacentCount == 2)):
					stillOk = 0
					score = score - .5
					break
				else:
					score = score + .25
			# check if we have a square
			if(stillOk == 1):
				isSquare = 1
				score = score + (10 - score) # squares have a base score of 10
				score = score + adjacent # add the length of the square side
		else:
			score = score - numpy.absolute(opposing - sides[unequalSide])
	else:
		sides.append(distance(individual[1],individual[2]))
		sides.append(distance(individual[1],individual[3]))
		sides.append(distance(individual[2],individual[3]))
		for x in range(0,len(sides)-1):
			for y in range(0,len(sides)-1):
				if ( x == y ):
					continue
					
				if(sides[x] == sides[y]):
					score = score + .5
					
	
	# Make sure non squares do not score over ten
	while(score >= 10 and isSquare == 0):
		score = score - 1
	return score
	
def grade(pop):
	sum = 0
	i = 0
	for x in pop:
		sum = sum + fitness(list(x))
		i = i + 1
	return sum / (len(pop) * 1.0)
	
def evolve(pop, retain = .2, random_select = .1, mutate = .02):
	graded = [(fitness(x),x) for x in pop]
	graded = [ x[1] for x in sorted(graded,key=lambda grade: grade[0],reverse=True)]
	retain_length = int(len(graded)*retain)
	parents = graded[:retain_length]

	# randomly add others for genetic diversity
	for individual in graded[retain_length:]:
		if( random_select > random() ):
			parents.append(individual)
	
	# mutate some
	for individual in parents:
		if(mutate > random()):
			pos_to_mutate = randint(0,len(individual)-1)
			exists = True
			mutCoord = 0
			while exists:
				mutCoord = Coord(randint(-10,10),randint(-10,10),'rx')
				for b in range(len(individual)):
					if( (mutCoord.x == individual[b].x) and (mutCoord.y == individual[b].y) ):
						exists = True
						break
					else:
						exists = False
			individual[pos_to_mutate] = mutCoord
	
	parents_length = len(parents)
	desired_length = len(pop) - parents_length
	children = []
	while len(children) < desired_length:
		male = randint(0, parents_length-1)
		female = randint(0,parents_length-1)
		if(male != female):
			male = parents[male]
			female = parents[female]
			half = int(len(male) / 2)
			child = []
			while (len(child) < 4):
				# Dad on Points 1 and 3
				if(len(child) == 0 or len(child) == 2):
					if(len(child) == 0):
						pos = randint(0,3)
						child.append(male[pos])
					else:
						exists = True
						pos = 0
						while exists:
							pos = randint(0,3)
							for b in range(len(child)):
								if((male[pos].x == child[b].x) and (male[pos].y == child[b].y)):
									exists = True
									break
								else:
									exists = False
						child.append(male[pos])
				# Mom on Points 2 and 4
				elif(len(child) == 1 or len(child) == 3):
					exists = True
					pos = 0
					while exists:
						pos = randint(0,3)
						for b in range(len(child)):
							if((female[pos].x == child[b].x) and (female[pos].y == child[b].y)):
								exists = True
								break
							else:
								exists = False
					child.append(female[pos])
			children.append(child)
	parents.extend(children)
	return list(parents)

# def PrintUsage():
	# print('Usage: 

def main(argv = sys.argv):	
	print('Creating Population...')
	p = population(100,-10,10)
	print('Generation #0')
	fitness_history = [grade(p),]
	# Show Best and Worst in the beginning for comparison
	print('------------------------------')
	graded = [(fitness(x),x) for x in p]
	graded = [ x[1] for x in sorted(graded,key=lambda grade: grade[0],reverse=True)]
	bestest = graded[0]
	worst = graded[len(graded)-1]
	print('Most Square')
	print(fitness(bestest))
	print('Coordinates:')
	for i in range(len(bestest)):
		print('Coord #'+str(i+1)+': ('+str(bestest[i].x)+', '+str(bestest[i].y)+')')
	plt.plot(bestest[0].x,bestest[0].y,bestest[0].options,bestest[1].x,bestest[1].y,bestest[1].options,bestest[2].x,bestest[2].y,bestest[2].options,bestest[3].x,bestest[3].y,bestest[3].options)
	plt.xlim(-11,11)
	plt.ylim(-11,11)
	plt.show()
	plt.clf()
	print('')
	print('Least Square')
	print(fitness(worst))
	print('Coordinates:')
	for i in range(len(worst)):
		print('Coord #'+str(i+1)+': ('+str(worst[i].x)+', '+str(worst[i].y)+')')
	plt.plot(worst[0].x,worst[0].y,worst[0].options,worst[1].x,worst[1].y,worst[1].options,worst[2].x,worst[2].y,worst[2].options,worst[3].x,worst[3].y,worst[3].options)
	plt.xlim(-11,11)
	plt.ylim(-11,11)
	plt.show()
	plt.clf()
	print('------------------------------')
	# Now run the genetic Algorithm
	for i in range(200):
		print('Generation #'+str(i+1))
		p = evolve(p)
		fitness_history.append(grade(p))
		
	print('Average Fitness per Generation')
	print('------------------------------')
	for datum in range(len(fitness_history)):
		print('Generation #'+str(datum)+': '+str(fitness_history[datum]))
	
	# Print end stats
	print('------------------------------')
	print('Population Size: '+ str(len(p)))
	graded = [(fitness(x),x) for x in p]
	graded = [ x[1] for x in sorted(graded,key=lambda grade: grade[0],reverse=True)]
	bestest = graded[0]
	worst = graded[len(graded)-1]
	print('Most Square')
	print(fitness(bestest))
	print('Coordinates:')
	for i in range(len(bestest)):
		print('Coord #'+str(i+1)+': ('+str(bestest[i].x)+', '+str(bestest[i].y)+')')
	plt.plot(bestest[0].x,bestest[0].y,bestest[0].options,bestest[1].x,bestest[1].y,bestest[1].options,bestest[2].x,bestest[2].y,bestest[2].options,bestest[3].x,bestest[3].y,bestest[3].options)
	plt.xlim(-11,11)
	plt.ylim(-11,11)
	plt.show()
	plt.clf()
	print('')
	print('Least Square')
	print(fitness(worst))
	print('Coordinates:')
	for i in range(len(worst)):
		print('Coord #'+str(i+1)+': ('+str(worst[i].x)+', '+str(worst[i].y)+')')
	plt.plot(worst[0].x,worst[0].y,worst[0].options,worst[1].x,worst[1].y,worst[1].options,worst[2].x,worst[2].y,worst[2].options,worst[3].x,worst[3].y,worst[3].options)
	plt.xlim(-11,11)
	plt.ylim(-11,11)
	plt.show()
	
	# x = []
	# x.append(Coord(0,0,'bo'))
	# x.append(Coord(1,0,'bo'))
	# x.append(Coord(0,1,'bo'))
	# x.append(Coord(1,1,'bo'))
	# print(fitness(x))
	
# Invoke the Main Routine
#--------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
#--------------------------------------------------------------------------------------