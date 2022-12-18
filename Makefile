CC = g++

CFLAGS = -g -Wall

all: findBestRouth

findBestRouth: findBestRouth.o
	$(CC) $(CFLAGS) -o findBestRouth findBestRouth.o
# g++ -g -Wall -o findBestRouth findBestRouth.o tinyxml2.o 

findBestRouth.o: findBestRouth.cpp findBestRouth.h
	$(CC) $(CFLAGS) -c findBestRouth.cpp
# g++ -g -Wall -c findBestRouth.cpp findBestRouth.h

clean:
	rm *.o findBestRouth