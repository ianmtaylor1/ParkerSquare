warnings = -Wall -Wextra
libs = -lgmp
opts = -O2

# Main targets
all: parkersquare test

clean:
	$(RM) -v parkersquare test *.o

# Executables
parkersquare: main.o primes.o squares.o search.o
	gcc $^ $(libs) -o $@

test: test.o primes.o squares.o search.o 
	gcc $^ $(libs) -o $@

# Objects
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