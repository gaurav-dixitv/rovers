CXX =	g++
CXXFLAGS =	-Wall -Werror -Wextra -pedantic		\
			-std=c++17 \

LDFLAGS =	-lm
BUILD =	./build
OBJ_DIR =	$(BUILD)/objects
BIN_DIR =	$(BUILD)/bin
TARGET =	rovers
INCLUDE =	-Iinclude/ -Ilibs/
entry = test
SRC =	\
		$(wildcard src/*.cpp)	\
		$(wildcard src/core/*.cpp)	\
		$(wildcard test/$(entry).cpp)	\

OBJECTS =$(SRC:%.cpp=$(OBJ_DIR)/%.o)

all: build $(BIN_DIR)/$(TARGET)

$(OBJ_DIR)/%.o: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@ $(LDFLAGS)

$(BIN_DIR)/$(TARGET):	$(OBJECTS)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -o $(BIN_DIR)/$(TARGET) $^ $(LDFLAGS)

.PHONY: all build clean debug release

build:
	@mkdir -p $(BIN_DIR)
	@mkdir -p $(OBJ_DIR)

debug: CXXFLAGS += -DDEBUG -g
debug: all

release: CXXFLAGS += -O2 -march=native -fopenmp
release: all

clean:
	-@rm -rvf $(OBJ_DIR)/*
	-@rm -rvf $(BIN_DIR)/*
