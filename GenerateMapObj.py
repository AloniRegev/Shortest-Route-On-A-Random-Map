import math
import os
import subprocess
from os import path
from random import randint
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

import matplotlib.pyplot as plt
from win32api import GetSystemMetrics

MIN_NO_OF_VER = 3
MAX_NO_OF_VER = 10


class Map:
    def __init__(self, _weight=None, _height=None, _start_point=None, _target_point=None, _polygons=None,
                 state="random"):
        """

        :param state: set the start_point and target_point randomly or fixed.

        If set to "random" then it wil generate random points.
        If set to "debug" then it fix the
            start_point to (0, 0) (bottom left corner)
            and target_point to (max_weight, max_height) (top right corner).
        It set to "random" by default.
        """
        if _weight is None:
            if state == "random":
                self.weight = randint(0, GetSystemMetrics(0))
            elif state == "debug":
                self.weight = 100
        else:
            self.weight = _weight

        if _height is None:
            if state == "random":
                self.height = randint(0, GetSystemMetrics(1))
            elif state == "debug":
                self.height = 100
        else:
            self.height = _height

        if _polygons is None:
            self.polygons = self.generate_polygons(state)
        else:
            self.polygons = _polygons

        if _start_point is None and _target_point is None:
            if state == "random":
                self.start_point = self.generate_point()
                self.target_point = self.generate_point()

            elif state == "debug":
                self.start_point = (0, 0)
                self.target_point = (self.weight, self.height)
        else:
            self.start_point = _start_point
            self.target_point = _target_point

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

    def generate_polygons(self, state="random", max_rad=100):
        """
        Class function that generate polygon objects of the Map object.
        It runs on the creation of a new Map object.

        :param state: 
        :param max_rad: maximum radius length from polygon center point to its vertexes.
        :return: list of polygon of the self Map object.
        """
        num_of_poly = 0
        if state == "debug":
            num_of_poly = randint(0, 10)  # generate number of polygons in map

        elif state == "random":
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
                                            radius, state=state))  # todo: change to dinemic num_of_vertices
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

    def __init__(self, _map=None, _center_point=None, _num_of_vertices=0, _max_rad=None, _vertices=None,
                 state="random"):
        if _vertices is None:
            _vertices = []
        self.map = _map
        self.center_point = _center_point
        self.num_of_vertices = _num_of_vertices
        if state == "debug":
            self.maxRad = 10
        else:
            self.maxRad = _max_rad

        if not _vertices:
            self.vertices = self.generate_vertices()
        else:
            self.vertices = _vertices

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
        vertices_list = []
        for i in range(self.num_of_vertices):
            radius = randint(0, self.maxRad)
            direction = randint(0, 360)

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

    def visual_maps(self, _map_list, is_polygon):
        """
        Visualization of each Map object from map_list one at a time using visualization method.
        """
        for m in _map_list:
            self.visualization(m, is_polygon)

    @staticmethod
    def visualization(_map, is_polygon):
        """
        Visualization of Map object.

        :param is_polygon: 
        :param _map: Map object to show on plot.
        """
        fig, ax = plt.subplots()

        ax.plot(_map.start_point[0], _map.start_point[1], 'o', color="magenta")  # plot start point
        ax.annotate("Start", _map.start_point)  # print label
        ax.plot(_map.target_point[0], _map.target_point[1], 'o', color="magenta")  # plot target point
        ax.annotate("Target", _map.target_point)  # print label

        # plot polygon representation
        for poly in _map.polygons:
            if is_polygon:
                ax = ControlManager.visual_polygon(ax, poly)
            else:
                ax = ControlManager.visual_obstacle(ax, poly)
                # for ver in poly.vertices:
                #     ax.plot(ver[0], ver[1], 'o', color="blue")

        ax.set_aspect(1)
        # ratio=1.0
        # print(abs((_map.get_weight() - 0) / (_map.get_height() - 0)) * ratio)
        # ax.set_aspect(abs((_map.get_weight() - 0) / (_map.get_height() - 0)) * ratio)

        plt.show()

    @staticmethod
    def visual_polygon(ax, poly):
        ax.plot(poly.center_point[0], poly.center_point[1], 'o', color="black")
        circle_plot = plt.Circle(poly.center_point, poly.maxRad, fill=False, color="green")

        ax.add_patch(circle_plot)  # print circle
        for ver in poly.vertices:
            ax.plot(ver[0], ver[1], 'o', color="blue")
        return ax

    @staticmethod
    def visual_obstacle(ax, poly):
        xs = []
        ys = []

        for val in poly.get_vertices():
            xs.append(val[0])
            ys.append(val[1])
        xs.append(xs[0])
        ys.append(ys[0])

        ax.plot(xs, ys, color="blue")
        return ax

    def output_maps(self, _xml_name="mapGenerator.xml"):
        """
        Create input XML file for algorithm program to read.

        :param _xml_name: name of the xml file to be created that stores the objects' data.
        """
        root = Element("Root")
        polygons_xml = SubElement(root, "Maps", size=str(len(self.map_list)))

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

        polygons_xml = SubElement(map_xml, 'Polygons', size=str(len(_map.get_poly())))

        for polygonNum, polygon in enumerate(_map.get_poly()):
            polygon_xml = SubElement(polygons_xml, 'Polygon', name=str(polygonNum))

            vertexes_xml = SubElement(polygon_xml, 'Vertexes', size=str(len(polygon.get_vertices())))
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

    def read_xml(self, _in_path="algorithmOutput.xml"):
        """
        create a new map element from given xml file path.

        :param _in_path: path of the xml output file of the algorithmic part .
        """
        tree = ElementTree.parse(_in_path)
        root = tree.getroot()

        map_list = []

        for m in root.iter('Map'):
            weight = int(m.find("./Weight").text)
            height = int(m.find("./Height").text)
            start_point = (int(m.find("./StartPoint/X").text), int(m.find("./StartPoint/Y").text))
            target_point = (int(m.find("./TargetPoint/X").text), int(m.find("./TargetPoint/Y").text))
            obstacles = []
            for o in m.iter('Obstacle'):
                vertices = []
                for v in o.iter('Vertex'):
                    vertices.append((int(v.find("./X").text), int(v.find("./Y").text)))
                obstacle = Polygon(_num_of_vertices=len(vertices), _vertices=vertices)
                obstacles.append(obstacle)
            _map = Map(weight, height, start_point, target_point, obstacles)
            map_list.append(_map)

        self.visual_maps(map_list, is_polygon=False)

    @staticmethod
    def run_cpp(_out_path="mapGenerator.xml", _in_path=".\\algorithmOutput.xml"):
        """
        function that creates the xml input file for the algorithm program, compile  the algorithm program cpp file
        and runs it with it's xml as input.

        :param _out_path: name for the xml file to be created as the input file of the algorithm program.
        :param _in_path: name for the xml file to be received from the algorithm program.
        """
        control.output_maps(_out_path)  # create input file for the algorithm program.
        try:
            os.system("make")  # compile algorithm program c++ file.

            try:
                algo = subprocess.Popen(["./findBestRouth", _out_path, _in_path])  # run the algorithm program
                algo.wait()
            except:
                raise Exception("Cannot run \"findBestRouth.exe\" file.")

        except:
            raise Exception("Cannot compile \"findBestRouth.cpp\" file.")


if __name__ == "__main__":
    control = ControlManager()  # create control object for data passing.
    control.add_map(Map(state="debug"))  # add new random Map to map_list.
    control.add_map(Map(state="debug"))  # add new random Map to map_list.
    control.run_cpp()  # create input file ,compile the algorithm program and runs it.
    control.visual_maps(control.get_map_list(), is_polygon=True)  # visual all Maps in map_list.
    control.read_xml()  # read xml file and plot map of it.
