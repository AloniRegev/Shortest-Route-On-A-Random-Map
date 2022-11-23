from random import randint
import math
import matplotlib.pyplot as plt
from win32api import GetSystemMetrics



MIN_NO_OF_VER=3
MAX_NO_OF_VER=10

class Map:
    def __init__(self):
        self.weight = randint(0,GetSystemMetrics(0))
        self.height = randint(0,GetSystemMetrics(1))
        self.polygons = self.generatePolygons()
        self.startPoint = self.generatePoint()
        self.targetPoint = self.generatePoint()
        # self.startPoint = (randint(0, self.weight), randint(0, self.height))
        # self.targetPoint = (randint(0, self.weight), randint(0, self.height))

    # def __init__(self, height, weight):
    #     self.height = height
    #     self.weight = weight
    #     self.startPoint = (randint(0,weight),randint(0,height))
    #     self.targetPoint = (randint(0,weight),randint(0,height))
    #     self.polygons = self.generatePolygons()
    #
    # def __init__(self, height, weight, polygons,  start, target):
    #     self.height = height
    #     self.weight = weight
    #     self.startPoint = start
    #     self.targetPoint = target
    #     self.polygons = polygons

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height=height

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight=weight

    def getPoly(self):
        return self.polygons

    def setPoly(self, polygons):
        self.polygons = polygons

    def generatePolygons(self,maxRad=100):
        numOfPoly= randint(0,int(math.sqrt(self.weight/maxRad)*int(self.height/maxRad)))  # generate number of polygons in map
        polygonList=[]

        while numOfPoly>0:
            centerPoint=(randint(0,self.weight), randint(0 ,self.height))
            radius=randint(MIN_NO_OF_VER, maxRad)
            validPolyLoc=True

            for recentPoly in polygonList:
                if abs(centerPoint[0] - recentPoly.centerPoint[0]) < radius+recentPoly.maxRad and abs(centerPoint[1] - recentPoly.centerPoint[1]) < radius+recentPoly.maxRad:
                    validPolyLoc=False
                    break

            if validPolyLoc:
                polygonList.append(Polygon(self, centerPoint, randint(MIN_NO_OF_VER,MAX_NO_OF_VER), radius))  # todo: change to dinemic numOfVertices
                numOfPoly -= 1

        return polygonList

    def generatePoint(self):
        point=(0,0)
        generFlag=True
        while generFlag:
            point = (randint(0, self.weight), randint(0, self.height))
            generFlag=False
            for recentPoly in self.polygons:
                if ((recentPoly.centerPoint[0]+recentPoly.maxRad) > point[0] and (recentPoly.centerPoint[0]-recentPoly.maxRad) < point[0]) and ((recentPoly.centerPoint[1]+recentPoly.maxRad) > point[1] and (recentPoly.centerPoint[1]-recentPoly.maxRad) < point[1]):
                    generFlag=True
                    break

        return point

class Polygon:
    def __init__(self, map):
        self.map=map
        self.centerPoint = (0,0)
        self.numOfVertices = 0
        self.maxRad=0
        self.vertices= []

    def __init__(self, map, centerPoint, numOfVertices, maxRad):
        self.map = map
        self.centerPoint = centerPoint
        self.numOfVertices = numOfVertices
        self.maxRad=maxRad
        self.vertices= self.generateVertices()

    # def __init__(self, map, centerPoint, numOfVertices,maxRad, vertices):
    #     self.map = map
    #     self.centerPoint = centerPoint
    #     self.numOfVertices = numOfVertices
    #     self.maxRad = maxRad
    #     self.vertices = vertices

    def getCenter(self):
        return self.centerPoint

    def setCenter(self, center):
        self.centerPoint = center

    def getNumVertices(self):
        return self.numOfVertices

    def setNumVertices(self, num):
        self.numOfVertices = num

    def getVertices(self):
        return self.numOfVertices

    def setVertices(self, vertices):
        self.vertices = vertices

    def generateVertices(self):
        direction = 0
        verticesList=[]
        for i in range(self.numOfVertices):
            radiuse = randint(0, self.maxRad)
            direction= randint(direction, 360-(self.numOfVertices-i))

            #calculete the x,y coordinates of every vertex.
            x = int(self.centerPoint[0]+radiuse*math.cos(direction))
            y = int(self.centerPoint[1]+radiuse*math.sin(direction))

            #chack if not out of bounds of the map.
            x=min(self.map.weight, max(0,x))
            y=min(self.map.height, max(0,y))

            # add the vertex to the verticesList.
            verticesList.append((x,y))

        return verticesList

def visualization(map):

    fig, ax = plt.subplots()

    ax.plot(map.startPoint[0], map.startPoint[1], 'o', color="magenta") # plot start point
    ax.annotate("Start", map.startPoint) #print lable
    ax.plot(map.targetPoint[0], map.targetPoint[1], 'o', color="magenta") # plot target point
    ax.annotate("Target", map.targetPoint) #print lable


    #plot polygon representation
    for poly in map.polygons:
        ax.plot(poly.centerPoint[0], poly.centerPoint[1], 'o', color="black")
        circlePlot=plt.Circle(poly.centerPoint, poly.maxRad,fill=False, color="green")

        ax.add_patch(circlePlot) #print circle
        for ver in poly.vertices:
            ax.plot(ver[0], ver[1], 'o', color="blue")
    ax.set_aspect('equal')
    plt.show()


if __name__ == "__main__":
    m=Map()
    print("dim: (", m.weight,", ", m.height,")")
    print("finish randomize")
    visualization(m)