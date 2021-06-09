OBJS	= a1q2.o
SOURCE	= a1q2.c
HEADER	= 
OUT	= a1q2_print
CC	 = gcc
FLAGS	 = -g -c -Wall
LFLAGS	 = -lpthread

all: $(OBJS)
	$(CC) -g $(OBJS) -o $(OUT) $(LFLAGS)

a1q2.o: a1q2.c
	$(CC) $(FLAGS) a1q2.c 


clean:
	rm -f $(OBJS) $(OUT)
