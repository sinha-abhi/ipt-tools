CC := g++
CXXFLAGS := -Wall -Wextra -std=c++11
TARGET := iptba

INC := include
SRC := iptba
BIN := bin

CXXFLAGS += -I$(INC)

all: | $(BIN)
	$(CC) $(CXXFLAGS) -o $(BIN)/$(TARGET) $(SRC)/*.cc

$(BIN):
	@mkdir -p $@

.PHONY: all

