CC = g++

CFLAGS = -g -Wall

all: main

main: main.cpp ControlManager.o tinyxml2.o
	$(CC) $(CFLAGS) -o findBestRouth main.cpp ControlManager.o tinyxml2.o

ControlManager.o: ControlManager.cpp ControlManager.h tinyxml2.o Map.o
	$(CC) $(CFLAGS) -c ControlManager.cpp

Map.o: Map.cpp Map.h Obstacle.o 
	$(CC) $(CFLAGS) -c Map.cpp Polygon.o Point.o

Obstacle.o: Obstacle.cpp Obstacle.h  Polygon.o
	$(CC) $(CFLAGS) -c Obstacle.cpp

Polygon.o: Polygon.cpp Polygon.h Point.o
	$(CC) $(CFLAGS) -c Polygon.cpp

Point.o: Point.cpp Point.h
	$(CC) $(CFLAGS) -c Point.cpp

tinyxml2.o: .\tinyxml2\tinyxml2.cpp .\tinyxml2\tinyxml2.h
	$(CC) $(CFLAGS) -c .\tinyxml2\tinyxml2.cpp

clean:
	rm *.o main