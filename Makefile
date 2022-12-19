CC = g++

CFLAGS = -g -Wall

all: main

# findBestRouth: main.o
# 	$(CC) $(CFLAGS) -o findBestRouth main.o

main: main.cpp ControlManager.o
	$(CC) $(CFLAGS) -o findBestRouth main.cpp
# g++ -g -Wall -o findBestRouth findBestRouth.o tinyxml2.o 

ControlManager.o: ControlManager.cpp ControlManager.h Map.o Polygon.o Obstacle.o Point.o tinyxml2.o 
	$(CC) $(CFLAGS) -c ControlManager.cpp
# g++ -g -Wall -c findBestRouth.cpp findBestRouth.h

	
Map.o: Map.cpp Map.h  Polygon.o Point.o
	$(CC) $(CFLAGS) -c Map.cpp Polygon.o Point.o

Obstacle.o: Obstacle.cpp Obstacle.h  Polygon.o Point.o
	$(CC) $(CFLAGS) -c Obstacle.cpp

Polygon.o: Polygon.cpp Polygon.h Point.o
	$(CC) $(CFLAGS) -c Polygon.cpp

Point.o: Point.cpp Point.h
	$(CC) $(CFLAGS) -c Point.cpp

tinyxml2.o: .\tinyxml2\tinyxml2.cpp .\tinyxml2\tinyxml2.h
	$(CC) $(CFLAGS) -c .\tinyxml2\tinyxml2.cpp

clean:
	rm *.o findBestRouth