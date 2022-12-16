import math
import os
from os import path
import subprocess
from random import randint
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

import matplotlib.pyplot as plt
from win32api import GetSystemMetrics

MIN_NO_OF_VER = 3
MAX_NO_OF_VER = 10


class Map:
    def __init__(self, state="random"):
        """

        :param state: set the start_point and target_point randomly or fixed.

        If set to "random" then it wil generate random points.
        If set to "debug" then it fix the
            start_point to (0, 0) (bottom left corner)
            and target_point to (max_weight, max_height) (top right corner).
        It set to "random" by default.
        """

        self.weight = randint(0, GetSystemMetrics(0))
        self.height = randint(0, GetSystemMetrics(1))
        self.polygons = self.generate_polygons()
        if state == "random":
            self.start_point = self.generate_point()
            self.target_point = self.generate_point()

        elif state == "debug":
            self.start_point = (0, 0)
            self.target_point = (self.weight, self.height)

    # def __init__(self, height, weight):
    #     self.height = height
    #     self.weight = weight
    #     self.start_point = (randint(0,weight),randint(0,height))
    #     self.targetPoint = (randint(0,weight),randint(0,height))
    #     self.polygons = self.generate_polygons()
    #
    # def __init__(self, height, weight, polygons,  start, target):
    #     self.height = height
    #     self.weight = weight
    #     self.start_point = start
    #     self.targetPoint = target
    #     self.polygons = polygons

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height

    def get_weight(self):
        return self.weight

    # def setWeight(self, weightMap):
    #     self.weight=weightMap

    def get_start_point(self):
        return self.start_point

    # def set_start_point(self, start_point):
    #     self.start_point=start_point

    def get_target_point(self):
        return self.target_point

    def set_target_point(self, target_point):
        self.target_point = target_point

    def get_poly(self):
        return self.polygons

    def set_poly(self, polygons):
        self.polygons = polygons

    def generate_polygons(self, max_rad=100):
        """
        Class function that generate polygon objects of the Map object.
        It runs on the creation of a new Map object.

        :param max_rad: maximum radius length from polygon center point to its vertexes.
        :return: list of polygon of the self Map object.
        """
        num_of_poly = randint(0, int(math.sqrt(self.weight / max_rad) * int(
            self.height / max_rad)))  # generate number of polygons in map
        polygon_list = []

        while num_of_poly > 0:
            center_point = (randint(0, self.weight), randint(0, self.height))
            radius = randint(MIN_NO_OF_VER, max_rad)
            valid_poly_loc = True

            for recentPoly in polygon_list:
                if abs(center_point[0] - recentPoly.center_point[0]) < radius + recentPoly.maxRad and abs(
                        center_point[1] - recentPoly.center_point[1]) < radius + recentPoly.maxRad:
                    valid_poly_loc = False
                    break

            if valid_poly_loc:
                polygon_list.append(Polygon(self, center_point, randint(MIN_NO_OF_VER, MAX_NO_OF_VER),
                                            radius))  # todo: change to dinemic num_of_vertices
                num_of_poly -= 1

        return polygon_list

    def generate_point(self):
        """
        class function that generate point represented as a tuple on Map object.
        It runs on the creation of a new Polygon object.

        :return: tuple of X and Y coordination of a point in the Map object.
        """
        point = (0, 0)
        is_generated = False
        while not is_generated:
            point = (randint(0, self.weight), randint(0, self.height))
            is_generated = True
            for recentPoly in self.polygons:
                if ((recentPoly.center_point[0] + recentPoly.maxRad) > point[0] > (
                        recentPoly.center_point[0] - recentPoly.maxRad)) and (
                        (recentPoly.center_point[1] + recentPoly.maxRad) > point[1] > (
                        recentPoly.center_point[1] - recentPoly.maxRad)):
                    is_generated = False
                    break

        return point


class Polygon:
    def __init__(self, _map):
        self.map = _map
        self.center_point = (0, 0)
        self.num_of_vertices = 0
        self.maxRad = 0
        self.vertices = []

    def __init__(self, _map, _center_point, _num_of_vertices, _max_rad):
        self.map = _map
        self.center_point = _center_point
        self.num_of_vertices = _num_of_vertices
        self.maxRad = _max_rad
        self.vertices = self.generate_vertices()

    # def __init__(self, map, center_point, num_of_vertices,maxRad, vertices):
    #     self.map = map
    #     self.center_point = center_point
    #     self.num_of_vertices = num_of_vertices
    #     self.maxRad = maxRad
    #     self.vertices = vertices

    def get_center(self):
        return self.center_point

    def set_center(self, center):
        self.center_point = center

    def get_num_vertices(self):
        return self.num_of_vertices

    def set_num_vertices(self, num):
        self.num_of_vertices = num

    def get_vertices(self):
        return self.vertices

    def set_vertices(self, vertices):
        self.vertices = vertices

    def generate_vertices(self):
        """
        class function that generate polygon vertexes.
        It runs on the creation of a new Polygon object.

        :return: vertexes list of the self polygon object.
        """
        direction = 0
        vertices_list = []
        for i in range(self.num_of_vertices):
            radius = randint(0, self.maxRad)
            direction = randint(direction, 360 - (self.num_of_vertices - i))

            # calculate the x,y coordinates of every vertex.
            x = int(self.center_point[0] + radius * math.cos(direction))
            y = int(self.center_point[1] + radius * math.sin(direction))

            # check if not out of bounds of the map.
            x = min(self.map.weight, max(0, x))
            y = min(self.map.height, max(0, y))

            # add the vertex to the verticesList.
            vertices_list.append((x, y))

        return vertices_list


class ControlManager:

    def __init__(self):
        self.map_list = []

    def add_map(self, _map):
        """
        Add Map object to map_list.

         :param _map: Map object.
        """
        self.map_list.append(_map)

    def get_map_list(self):
        """
        Get function to map_list.
        """
        return self.map_list

    def visual_maps(self):
        """
        Visualization of each Map object from map_list one at a time using visualization method.
        """
        for m in self.get_map_list():
            print("dim: (", m.weight, ", ", m.height, ")")
            self.visualization(m)

    @staticmethod
    def visualization(_map):
        """
        Visualization of Map object.

        :param _map: Map object to show on plot.
        """
        fig, ax = plt.subplots()

        ax.plot(_map.start_point[0], _map.start_point[1], 'o', color="magenta")  # plot start point
        ax.annotate("Start", _map.start_point)  # print label
        ax.plot(_map.target_point[0], _map.target_point[1], 'o', color="magenta")  # plot target point
        ax.annotate("Target", _map.target_point)  # print label

        # plot polygon representation
        for poly in _map.polygons:
            ax.plot(poly.center_point[0], poly.center_point[1], 'o', color="black")
            circle_plot = plt.Circle(poly.center_point, poly.maxRad, fill=False, color="green")

            ax.add_patch(circle_plot)  # print circle
            for ver in poly.vertices:
                ax.plot(ver[0], ver[1], 'o', color="blue")
        ax.set_aspect('equal')
        plt.show()

    def output_maps(self, _xml_name="mapGenerator.xml"):
        """
        Create input XML file for algorithm program to read.

        :param _xml_name: name of the xml file to be created that stores the objects' data.
        """
        root = Element("map_list")

        polygons_xml = SubElement(root, "Maps")

        for i, _map in enumerate(self.map_list):
            self.output_map_attributes(i, _map, polygons_xml)

        # write to file
        out_file = open(path.join(os.getcwd(), _xml_name), "w", encoding='utf8')  # overnight file
        for line in self.prettify(root).split("\n"):
            out_file.write(line)

        out_file.close()

    @staticmethod
    def output_map_attributes(_map_name, _map, _maps_xml):
        """
        Append map object for the input file to for algorithm program to read.

        :param _map_name: number of map in the list for loop tracking.
        :param _map: Map object to add to file.
        :param _maps_xml: xml tree object to make sub element to. 
        """
        map_xml = SubElement(_maps_xml, 'Map', name=str(_map_name))
        weight = SubElement(map_xml, 'Weight')
        weight.text = str(_map.get_weight())
        height = SubElement(map_xml, 'Height')
        height.text = str(_map.get_height())

        start_point = SubElement(map_xml, 'StartPoint')
        xs = SubElement(start_point, 'X')
        xs.text = str(_map.get_start_point()[0])
        ys = SubElement(start_point, 'Y')
        ys.text = str(_map.get_start_point()[1])

        target_point = SubElement(map_xml, 'TargetPoint')
        xs = SubElement(target_point, 'X')
        xs.text = str(_map.get_target_point()[0])
        ys = SubElement(target_point, 'Y')
        ys.text = str(_map.get_target_point()[1])

        polygons_xml = SubElement(map_xml, 'Polygons')

        for polygonNum, polygon in enumerate(_map.get_poly()):
            polygon_xml = SubElement(polygons_xml, 'Polygon', name=str(polygonNum))

            vertexes_xml = SubElement(polygon_xml, 'Vertexes')
            for vertexName, vertex in enumerate(polygon.get_vertices()):
                vertex_xml = SubElement(vertexes_xml, 'Vertex', name=str(vertexName))
                xs = SubElement(vertex_xml, 'X')
                xs.text = str(vertex[0])
                ys = SubElement(vertex_xml, 'Y')
                ys.text = str(vertex[1])

    @staticmethod
    def prettify(elem):
        """
        Return a pretty-printed XML string for the Element.

        :param elem: ElementTree object to convert to string.
        """
        rough_string = ElementTree.tostring(elem, encoding='unicode')
        reparse = minidom.parseString(rough_string)
        return reparse.toprettyxml(indent="  ")

    @staticmethod
    def run_cpp(_xml_name="mapGenerator.xml"):
        """
        function that creates the xml input file for the algorithm program, compile  the algorithm program cpp file
        and runs it with it's xml as input.

        :param _xml_name: name for the xml file to be created as the input file of the algorithm program.
        """

        control.output_maps(_xml_name)
        if os.system("g++ -g -Wall -o findBestRouth  findBestRouth.cpp") == 0:  # todo replace it with makefile call
            try:
                proc = subprocess.Popen(["./findBestRouth", _xml_name])

            except:
                raise Exception("Cannot run \"findBestRouth.exe\" file.")
        else:
            raise Exception("Cannot compile \"findBestRouth.cpp\" file.")


if __name__ == "__main__":
    control = ControlManager()              # create control object for data passing
    control.add_map(Map(state="debug"))     # add new random Map to map_list
    control.add_map(Map(state="debug"))     # add new random Map to map_list
    control.visual_maps()                   # visual all Maps in map_list
    control.run_cpp()                       # create input file ,compile the algorithm program and runs it.
