warnings = -Wall -Wextra
libs = -lgmp
opts = -O1

all: parkersquare test

parkersquare: main.o primes.o squares.o search.o
	gcc $^ $(libs) -o $@

test: test.o primes.o squares.o search.o 
	gcc $^ $(libs) -o $@

primes.o: primes.c primes.h
	gcc -c $(opts) $(warnings) -o $@ $<

squares.o: squares.c squares.h primes.h
	gcc -c $(opts) $(warnings) -o $@ $<

search.o: search.c search.h squares.h primes.h
	gcc -c $(opts) $(warnings) -o $@ $<

main.o: main.c search.h squares.h primes.h
	gcc -c $(opts) $(warnings) -o $@ $<

test.o: test.c search.h squares.h primes.h
	gcc -c $(opts) $(warnings) -o $@ $<