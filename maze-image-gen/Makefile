CXXFLAGS := -I /usr/include/opencv4 -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -Wshadow -Wall -Wextra -O3 -march=native
mazegen: main.cpp
	$(CXX) $(CXXFLAGS) $? -o $@

clean:
	-rm -rf mazegen

.PHONY: clean mazegen
