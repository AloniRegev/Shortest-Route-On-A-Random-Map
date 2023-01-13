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


class Point:
    """
    class that represent Point object.
    """

    def __init__(self, coordinates, line_of_sight=None):
        """

        :param
        coordinates: x and y coordinate values of the point.
        line_of_sight: A list of all the points that can be seen from the current point.
        """
        self.coordinates = coordinates
        self.line_of_sight = line_of_sight if line_of_sight else []

    def get_coordinates(self):
        return self.coordinates

    def get_line_of_sight(self):
        return self.line_of_sight

    def set_line_of_sight(self, line_of_sight):
        self.line_of_sight = line_of_sight


class Map:
    """
    class that represent a Map object.
    """

    def __init__(self, _width=None, _height=None, _start_point=None, _target_point=None, _polygons=None, _route=None,
                 state="random"):
        """

        :param
        _width: Map width value.
        _height: Map height value.
        _start_point: Start_point value.
        _target_point: Target_point value.
        _polygons: A list of all the polygons on the map. If no list is defined it will automatically draw polygons.
        _route: A list of the points describing the easiest route.
        state: set the start_point and target_point randomly or fixed.

        If set to "random" then it wil generate random points.
        If set to "debug" then it fix the
            start_point to (0, 0) (bottom left corner)
            and target_point to (max_weight, max_height) (top right corner).
        It set to "random" by default.
        """
        self.routh = None
        if _width is None:
            if state == "random":
                self.width = randint(100, GetSystemMetrics(0))
            elif state == "debug":
                self.width = 100
        else:
            self.width = _width

        if _height is None:
            if state == "random":
                self.height = randint(100, GetSystemMetrics(1))
            elif state == "debug":
                self.height = 100
        else:
            self.height = _height

        self.polygons = self.generate_polygons(state) if _polygons is None else _polygons

        if _start_point is None and _target_point is None:
            if state == "random":
                self.start_point = self.generate_point()
                self.target_point = self.generate_point()

            elif state == "debug":
                self.start_point = Point((0, 0))
                self.target_point = Point((self.width, self.height))
        else:
            self.start_point = _start_point
            self.target_point = _target_point

        self.route = _route if _route else []

    # getters and setters.
    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height

    def get_weight(self):
        return self.width

    def get_start_point(self):
        return self.start_point

    def get_target_point(self):
        return self.target_point

    def set_target_point(self, target_point):
        self.target_point = target_point

    def get_routh(self):
        return self.route

    def set_routh(self, routh):
        self.routh = routh

    def get_poly(self):
        return self.polygons

    def set_poly(self, polygons):
        self.polygons = polygons

    # class functions.
    def generate_polygons(self, state="random", max_rad=300):
        """
        Class function that generate polygon objects of the Map object.
        It runs on the creation of a new Map object.

        :param state: set the start_point and target_point randomly or fixed.
        :param max_rad: maximum radius length from polygon center point to its vertexes.
        :return: list of polygon of the self Map object.
        """
        num_of_poly = 0
        if state == "debug":
            num_of_poly = randint(0, 40)  # generate number of polygons in map
            # num_of_poly = 40  # generate number of polygons in map

        elif state == "random":
            num_of_poly = randint(0, int(math.sqrt(self.width / max_rad) * int(
                self.height / max_rad)))  # generate number of polygons in map

        polygon_list = []

        timer = 0
        while num_of_poly > 0:
            center_point = randint(0, self.width), randint(0, self.height)
            radius = randint(MIN_NO_OF_VER, max_rad)
            valid_poly_loc = True

            for recentPoly in polygon_list:
                x, y = recentPoly.center_point.get_coordinates()
                if abs(center_point[0] - x) < radius + recentPoly.maxRad and abs(
                        center_point[1] - y) < radius + recentPoly.maxRad:
                    valid_poly_loc = False
                    break

            if valid_poly_loc:
                polygon_list.append(
                    Polygon((self.width, self.height), center_point, randint(MIN_NO_OF_VER, MAX_NO_OF_VER),
                            radius, state=state))
            if valid_poly_loc or timer % 100 == 0:
                num_of_poly -= 1

            timer += 1

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
            point = (randint(0, self.width), randint(0, self.height))
            is_generated = True
            for recentPoly in self.polygons:
                x, y = recentPoly.center_point.get_coordinates()
                if ((x + recentPoly.maxRad) > point[0] > (x - recentPoly.maxRad)) \
                        and ((y + recentPoly.maxRad) > point[1] > (y - recentPoly.maxRad)):
                    is_generated = False
                    break

        return Point(point)


class Polygon:
    """
    class that represent polygon object.
    """

    def __init__(self, _dimension=None, _center_point=None, _num_of_vertices=0, _max_rad=None, _vertices=None,
                 state="random"):
        """

        :param
        _dimension: A tuple describing the map dimensions (width, height) of the map the polygon is related to.
        _center_point: The center point of the polygon.
        _num_of_vertices: The number of vertices in the polygon.
        _max_rad: The size of the maximum radius that the polygon can draw.
        _vertices: A list of vertices in a polygon. If no list is passed,
                    it will automatically draw vertices into a polygon.
        state: set the start_point and target_point randomly or fixed.

        If set to "random" then it wil generate random points.
        If set to "debug" then it fix the
            start_point to (0, 0) (bottom left corner)
            and target_point to (max_weight, max_height) (top right corner).
        It set to "random" by default.
        """
        if _vertices is None:
            _vertices = []
        self.dimension = _dimension if _dimension else (100, 100)
        self.center_point = Point(_center_point)
        self.num_of_vertices = _num_of_vertices
        if state == "debug":
            self.maxRad = 15
        else:
            self.maxRad = _max_rad

        self.vertices = self.generate_vertices() if not _vertices else _vertices

    # getters and setters.
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

    # class functions
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
            x = int(self.center_point.get_coordinates()[0] + radius * math.cos(direction))
            y = int(self.center_point.get_coordinates()[1] + radius * math.sin(direction))

            # check if not out of bounds of the map.
            x = min(self.dimension[0], max(0, x))
            y = min(self.dimension[1], max(0, y))

            # add the vertex to the verticesList.
            vertices_list.append(Point((x, y)))

        return vertices_list


class ControlManager:
    """
    A class that serves as a user interface for creating map type objects
    and managing the communication between the 2 parts of the project.
    """

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
    def visualization(_map, is_from_input):
        """
        Visualization of Map object.

        :param _map: Map object to show on plot.
        :param is_from_input: A flag describing whether the resulting map object
                is from a draw or a receiver from the reading xml.
        """
        fig, ax = plt.subplots()

        # plot polygon representation
        for poly in _map.polygons:
            if is_from_input:  # plot for reading from xml.
                ControlManager.visual_los(ax, _map.get_start_point())
                for ver in poly.get_vertices():
                    ControlManager.visual_los(ax, ver)
                ControlManager.visual_obstacle(ax, poly)

            else:  # plot for drawn map.
                ControlManager.visual_polygon(ax, poly)
        if is_from_input:  # plot for reading from xml.
            ControlManager.visual_routh(ax, _map.get_routh())  # Show routh.

        ax.plot(_map.start_point.get_coordinates()[0], _map.start_point.get_coordinates()[1], 'o',
                color="gold")  # plot start point
        ax.annotate("Start", _map.start_point.get_coordinates())  # print label
        ax.plot(_map.target_point.get_coordinates()[0], _map.target_point.get_coordinates()[1], 'o',
                color="#00D100")  # plot target point
        ax.annotate("Target", _map.target_point.get_coordinates())  # print label

        ax.set_aspect(1)
        plt.show()

    @staticmethod
    def visual_polygon(ax, poly):
        """
        A helper function that plots a drawn polygon type object.
        :param ax: subplots reference to add objects to.
        :param poly: polygon object to plot.
        """
        ax.plot(poly.center_point.get_coordinates()[0], poly.center_point.get_coordinates()[1], 'o', color="black")
        circle_plot = plt.Circle(poly.center_point.get_coordinates(), poly.maxRad, fill=False, color="green")

        ax.add_patch(circle_plot)  # print circle
        for ver in poly.vertices:
            ax.plot(ver.get_coordinates()[0], ver.get_coordinates()[1], 'o', color="blue")

    @staticmethod
    def visual_obstacle(ax, obstacle):
        """
        A helper function that plots a polygon object from the xml .
        :param ax: subplots reference to add objects to.
        :param obstacle: obstacle object to plot.
        """
        xs = []
        ys = []

        for val in obstacle.get_vertices():
            xs.append(val.get_coordinates()[0])
            ys.append(val.get_coordinates()[1])
        if xs and ys:
            xs.append(xs[0])
            ys.append(ys[0])

        ax.plot(xs, ys, color="blue", alpha=.5)
        ax.fill_between(xs, ys, 0, facecolor='blue', alpha=.5)
        ax.scatter(xs, ys, color="blue")

    @staticmethod
    def visual_los(ax, sp):
        """
        A helper function that plots a line of sight from the xml .
        :param ax: subplots reference to add objects to.
        :param sp: point to plot the line of sight
        """
        los = sp.get_line_of_sight()
        x, y = sp.get_coordinates()
        if los:
            for v in los:
                xs = [x, v.get_coordinates()[0]]
                ys = [y, v.get_coordinates()[1]]
                ax.plot(xs, ys, color="WhiteSmoke")

    @staticmethod
    def visual_routh(ax, routh):
        """
        A helper function that plots a routh path from the xml .

        :param ax: subplots reference to add objects to.
        :param routh: An ordered list of nodes from the start node to the goal node.
        """
        xs = []
        ys = []
        for ver in routh:
            xs.append(ver.get_coordinates()[0])
            ys.append(ver.get_coordinates()[1])

        ax.plot(xs, ys, color="red")

    def write_xml(self, _xml_name):
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
        xs.text = str(_map.get_start_point().get_coordinates()[0])
        ys = SubElement(start_point, 'Y')
        ys.text = str(_map.get_start_point().get_coordinates()[1])

        target_point = SubElement(map_xml, 'TargetPoint')
        xs = SubElement(target_point, 'X')
        xs.text = str(_map.get_target_point().get_coordinates()[0])
        ys = SubElement(target_point, 'Y')
        ys.text = str(_map.get_target_point().get_coordinates()[1])

        polygons_xml = SubElement(map_xml, 'Polygons', size=str(len(_map.get_poly())))

        for polygonNum, polygon in enumerate(_map.get_poly()):
            polygon_xml = SubElement(polygons_xml, 'Polygon', name=str(polygonNum))

            vertexes_xml = SubElement(polygon_xml, 'Vertexes', size=str(len(polygon.get_vertices())))
            for vertexName, vertex in enumerate(polygon.get_vertices()):
                vertex_xml = SubElement(vertexes_xml, 'Vertex', name=str(vertexName))
                xs = SubElement(vertex_xml, 'X')
                xs.text = str(vertex.get_coordinates()[0])
                ys = SubElement(vertex_xml, 'Y')
                ys.text = str(vertex.get_coordinates()[1])

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
    def read_xml(_in_path):
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
            sp_los = []
            for sp in m.iter("StartPoint"):
                for v in sp.iter('Vertex'):
                    sp_los.append(Point((int(v.find("./X").text), int(v.find("./Y").text))))
            start_point = Point((int(m.find("./StartPoint/X").text), int(m.find("./StartPoint/Y").text)), sp_los)
            target_point = Point((int(m.find("./TargetPoint/X").text), int(m.find("./TargetPoint/Y").text)))
            obstacles = []
            for o in m.iter('Obstacle'):
                vertices = []
                for v in o.findall('.Vertexes/Vertex'):
                    ver = (int(v.find("./X").text), int(v.find("./Y").text))
                    p_los = []
                    for v_los in v.iter("Vertex"):
                        p_los.append(Point((int(v_los.find("./X").text), int(v_los.find("./Y").text))))
                    vertices.append(Point(ver, p_los))

                obstacle = Polygon(_num_of_vertices=len(vertices), _vertices=vertices)
                obstacles.append(obstacle)

            route = []
            for r in m.iter('Route'):
                for route_ver in r.iter('Vertex'):
                    route.append(Point((int(route_ver.find("./X").text), int(route_ver.find("./Y").text))))

            _map = Map(weight, height, start_point, target_point, obstacles, route)
            map_list.append(_map)

        return map_list

    @staticmethod
    def exe_program(_out_path: object, _in_path: object, state="random"):
        """
        function that creates the xml input file for the algorithm program, compile  the algorithm program cpp file
        and runs it with it's xml as input.

        :param _out_path: name for the xml file to be created as the input file of the algorithm program.
        :param _in_path: name for the xml file to be received from the algorithm program.
        """
        control.write_xml(_out_path)  # create input file for the algorithm program.
        try:
            if state == "debug" or not os.path.exists(path.join(os.getcwd(), "findBestRouth.exe")):
                os.system("make")  # compile algorithm program c++ file.

            try:
                algo = subprocess.Popen(
                    [path.join(os.getcwd(), "findBestRouth.exe"), _out_path, _in_path])  # run the algorithm program
                algo.wait()

            except:
                raise Exception("Cannot run \"findBestRouth.exe\" file.")

        except:
            raise Exception("Cannot compile \"main.cpp\" file.")


if __name__ == "__main__":
    _out_path = path.join(os.getcwd(), "Python_output.xml")
    _in_path = path.join(os.getcwd(), "cpp_output.xml")
    control = ControlManager()  # create control object for data passing.
    control.add_map(Map(state="debug",
                        _polygons=[
                            Polygon(_dimension=(100, 100), _center_point=(25, 35), _num_of_vertices=20, _max_rad=25),
                            Polygon(_dimension=(100, 100), _center_point=(75, 65), _num_of_vertices=20,
                                    _max_rad=25)]))  # add new Map to map_list.
    # control.add_map(Map(state="debug"))  # add new random Map to map_list.
    control.add_map(Map(state="random"))  # add new random Map to map_list.
    control.exe_program(_out_path, _in_path, state="debug")  # create input file ,compile the algorithm program and runs it.
    control.visual_maps(control.get_map_list(), is_polygon=False)  # visual all Maps in map_list.
    received_map_list = control.read_xml(_in_path)  # read xml file and plot map of it.
    control.visual_maps(received_map_list, is_polygon=True)
