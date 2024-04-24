# export LD_LIBRARY_PATH=`pwd`

CC = clang
CFLAGS = -Wall -pedantic -std=c99
LIBS = -lm

all: _phylib.so

clean:
	rm -f *.o *.so A1

_phylib.so: phylib.o libphylib.so phylib_wrap.o
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o $(LIBS)

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

test.o: A2test2.c phylib.h
	$(CC) $(CFLAGS) -c A2test2.c -o test.o

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -fPIC -I /usr/include/python3.11 -o phylib_wrap.o

main: test.o libphylib.so
	$(CC) test.o $(LIBS) -L. -lphylib -o A1