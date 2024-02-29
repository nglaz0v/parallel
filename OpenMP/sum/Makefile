
CC = gcc
CFLAGS = -fopenmp -Wall -std=c11
LDFLAGS = -fopenmp

TARGET = sum
OBJS = main.o isum.o

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $(TARGET) $(OBJS)

.PHONY: all
all: $(TARGET)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGET) $(OBJS)
