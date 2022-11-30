from random import randint
import math
import matplotlib.pyplot as plt
from win32api import GetSystemMetrics
import os
from os import path
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring
from xml.etree import ElementTree
from xml.dom import minidom


MIN_NO_OF_VER=3
MAX_NO_OF_VER=10

class Map:
    def __init__(self):
        self.weight = randint(0,GetSystemMetrics(0))
        self.height = randint(0,GetSystemMetrics(1))
        self.polygons = self.generatePolygons()
        self.startPoint = self.generatePoint()
        self.targetPoint = self.generatePoint()


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

    # def setWeight(self, weightMap):
    #     self.weight=weightMap

    def getStartPoint(self):
        return self.startPoint

    # def setStartPoint(self, startPoint):
    #     self.startPoint=startPoint

    def getEndPoint(self):
        return self.targetPoint

    def setEndPoint(self, targetPoint):
        self.targetPoint=targetPoint

    def getPoly(self):
        return self.polygons

    def setPoly(self, polygons):
        self.polygons = polygons

    def generatePolygons(self,maxRad=100):
        """
        Class function that generate polygon objects of the Map object.
        It runs on the creation of a new Map object.

        :param maxRad: maximum radius length from polygon center point to its vertexes.
        :return: list of polygon of the self Map object.
        """
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
        """
        class function that generate point represented as a tuple on Map object.
        It runs on the creation of a new Polygon object.

        :return: tuple of X and Y coordination of a point in the Map object.
        """
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
        return self.vertices

    def setVertices(self, vertices):
        self.vertices = vertices

    def generateVertices(self):
        """
        class function that generate polygon vertexes.
        It runs on the creation of a new Polygon object.

        :return: vertexes list of the self polygon object.
        """
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


class controlMenager:
    mapList=[]
    def __init__(self):
        mapList=[]


    def addMap(self, map):
        """
        Add Map object to mapList.

         :param map: Map object.
        """
        self.mapList.append(map)

    def getMapList(self):
        """
        Get function to mapList.
        """
        return self.mapList

    def visualMaps(self):
        """
        Visualization of each Map object from mapList one at a time using visualization metod.
        """
        for m in self.getMapList():
            print("dim: (", m.weight,", ", m.height,")")
            self.visualization(m)

    def visualization(self, map):
        """
        Visualization of Map object.

        :param map: Map object to show on plot.
        """
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

    def outputMaps(self):
        """
        Create input XML file for algorithm program to read.
        """
        root = Element("mapList")

        PolygonsXML = SubElement(root, "Maps")

        for i, map in enumerate(self.mapList):
            self.outputMapAttributs(i, map, PolygonsXML)

        #write to file
        outFile = open(path.join(os.getcwd(), "mapGenetrtor.xml"), "w", encoding='utf8')  # overnight file
        for line in self.prettify(root).split("\n"):
            outFile.write(line)

        outFile.close()


    def outputMapAttributs(self, mapName, map, mapsXML):
        """
        Append map object for the input file to for algorithm program to read.

        :param mapName: number of map in the list for loop tracking.
        :param map: Map object to add to file.
        """
        mapXML = SubElement(mapsXML, 'Map', name=str(mapName))
        weight = SubElement(mapXML, 'Weight')
        weight.text = str(map.getWeight())
        height = SubElement(mapXML, 'Height')
        height.text = str(map.getHeight())

        startPoint = SubElement(mapXML, 'StartPoint')
        Xs = SubElement(startPoint, 'X')
        Xs.text = str(map.getStartPoint()[0])
        Ys = SubElement(startPoint, 'Y')
        Ys.text = str(map.getStartPoint()[1])

        targetPoint = SubElement(mapXML, 'TargetPoint')
        Xs = SubElement(targetPoint, 'X')
        Xs.text = str(map.getEndPoint()[0])
        Ys = SubElement(targetPoint, 'Y')
        Ys.text = str(map.getEndPoint()[1])

        PolygonsXML = SubElement(mapXML, 'Polygons')

        for polygonNum, polygon in enumerate(map.getPoly()):
            PolygonXML = SubElement(PolygonsXML, 'Polygon', name=str(polygonNum))

            vertexesXML = SubElement(PolygonXML, 'Vertexes')
            for vertexName, vertex in enumerate(polygon.getVertices()):
                vertexXML = SubElement(vertexesXML, 'Vertex', name=str(vertexName))
                Xs=SubElement(vertexXML, 'X')
                Xs.text = str(vertex[0])
                Ys=SubElement(vertexXML, 'Y')
                Ys.text = str(vertex[1])


    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.

         :param elem: ElementTree object to convert to string.
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

if __name__ == "__main__":
    control = controlMenager() # create control object for data passing
    control.addMap(Map()) # add new random Map to Maplist
    control.addMap(Map()) # add new random Map to Maplist
    control.outputMaps() # creat output file for algoritem program to read
    control.visualMaps() # visual all Maps in Maplist


