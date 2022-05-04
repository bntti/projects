#include <iostream>
#include <opencv4/opencv2/opencv.hpp>
#include <random>
#include <vector>

struct Cell {
    bool visited;
    bool top_wall, right_wall, bottom_wall, left_wall;
    Cell() {
        visited = false;
        top_wall = true;
        right_wall = true;
        bottom_wall = true;
        left_wall = true;
    }
};
std::mt19937 rng(std::chrono::steady_clock::now().time_since_epoch().count());

const cv::Scalar BACKGROUND(255, 255, 255);
const cv::Scalar WALL(0, 0, 0);
const cv::Scalar START(0, 255, 0);
const cv::Scalar GOAL(255, 0, 0);

int width;
int height;
int cell_size;
cv::Point goal;
cv::Point start;
std::vector<std::vector<Cell>> cells;

std::vector<cv::Point> dirs = {
    cv::Point(-1, 0), cv::Point(1, 0),
    cv::Point(0, 1), cv::Point(0, -1)};

void drawRectangle(int x1, int y1, int x2, int y2, cv::Mat& image, cv::Scalar color) {
    cv::Point pt1(x1, y1);
    cv::Point pt2(x2, y2);
    cv::rectangle(image, pt1, pt2, color, -1);
}

void drawCell(int cell_x, int cell_y, cv::Mat& image) {
    int start_x = (cell_x + 1) * cell_size - cell_size + cell_x + 1;
    int end_x = start_x + cell_size - 1;
    int start_y = (cell_y + 1) * cell_size - cell_size + cell_y + 1;
    int end_y = start_y + cell_size - 1;

    if (cell_x == goal.x && cell_y == goal.y) {
        drawRectangle(start_x, start_y, end_x, end_y, image, GOAL);
    }
    if (cell_x == start.x && cell_y == start.y) {
        drawRectangle(start_x, start_y, end_x, end_y, image, START);
    }

    Cell cell = cells[cell_x][cell_y];
    if (cell.top_wall) {
        drawRectangle(start_x - 1, start_y - 1, end_x + 1, start_y - 1, image, WALL);
    }
    if (cell.bottom_wall) {
        drawRectangle(start_x - 1, end_y + 1, end_x + 1, end_y + 1, image, WALL);
    }
    if (cell.right_wall) {
        drawRectangle(end_x + 1, start_y - 1, end_x + 1, end_y + 1, image, WALL);
    }
    if (cell.left_wall) {
        drawRectangle(start_x - 1, start_y - 1, start_x - 1, end_y + 1, image, WALL);
    }
}

void draw() {
    cv::Mat image(
        height * cell_size + height + 1,
        width * cell_size + width + 1,
        CV_8UC3,
        BACKGROUND);

    for (int x = 0; x < width; ++x) {
        for (int y = 0; y < height; ++y) {
            drawCell(x, y, image);
        }
    }

    cv::imwrite("output.png", image);
}

void RemoveWall(cv::Point p1, cv::Point p2) {
    if (p1.x > p2.x) {
        cells[p1.x][p1.y].left_wall = false;
        cells[p2.x][p2.y].right_wall = false;
    }
    if (p1.x < p2.x) {
        cells[p1.x][p1.y].right_wall = false;
        cells[p2.x][p2.y].left_wall = false;
    }
    if (p1.y > p2.y) {
        cells[p1.x][p1.y].top_wall = false;
        cells[p2.x][p2.y].bottom_wall = false;
    }
    if (p1.y < p2.y) {
        cells[p1.x][p1.y].bottom_wall = false;
        cells[p2.x][p2.y].top_wall = false;
    }
}

// DFS generation
void DFS(cv::Point p1) {
    int x = p1.x;
    int y = p1.y;
    std::vector<cv::Point> shuffled_dirs = dirs;
    shuffle(shuffled_dirs.begin(), shuffled_dirs.end(), rng);

    for (cv::Point dir : shuffled_dirs) {
        int new_x = x + dir.x;
        int new_y = y + dir.y;
        if (0 <= new_x && new_x < width && 0 <= new_y && new_y < height && !cells[new_x][new_y].visited) {
            cv::Point p2(new_x, new_y);
            cells[p2.x][p2.y].visited = true;
            RemoveWall(p1, p2);
            DFS(p2);
        }
    }
}

void DFSMaze() {
    cells[start.x][start.y].visited = true;
    DFS(start);
}

// BFS generation
void AddNeighborPoints(std::vector<std::pair<cv::Point, cv::Point>>& points, cv::Point starting_point) {
    for (cv::Point dir : dirs) {
        int new_x = starting_point.x + dir.x;
        int new_y = starting_point.y + dir.y;
        if (0 <= new_x && new_x < width && 0 <= new_y && new_y < height && !cells[new_x][new_y].visited) {
            points.push_back({starting_point, cv::Point(new_x, new_y)});
        }
    }
}

void RandomBFSMaze() {
    std::vector<std::pair<cv::Point, cv::Point>> points;
    cells[start.x][start.y].visited = true;
    AddNeighborPoints(points, start);

    while (points.size() > 0) {
        int i = rng() % points.size();
        cv::Point p1 = points[i].first;
        cv::Point p2 = points[i].second;
        swap(points[i], points.back());
        points.pop_back();

        if (!cells[p2.x][p2.y].visited) {
            cells[p2.x][p2.y].visited = true;
            RemoveWall(p1, p2);
            AddNeighborPoints(points, p2);
        }
    }
}

// Recursive generation
void recursion(int x1, int y1, int x2, int y2) {
    if (x1 == x2) {
        for (int y = y1; y < y2; ++y) {
            RemoveWall(cv::Point(x1, y), cv::Point(x1, y + 1));
        }
        return;
    }
    if (y1 == y2) {
        for (int x = x1; x < x2; ++x) {
            RemoveWall(cv::Point(x, y1), cv::Point(x + 1, y1));
        }
        return;
    }
    // Split current area into four areas and leave a gap in three of the four walls
    int area_w = x2 - x1 + 1;
    int area_h = y2 - y1 + 1;
    int half_w = area_w / 2;
    int half_h = area_h / 2;
    int middle_x = x1 + half_w - 1;
    int middle_y = y1 + half_h - 1;

    std::vector<bool> inner_sides = {0, 1, 1, 1};
    std::shuffle(inner_sides.begin(), inner_sides.end(), rng);

    if (inner_sides[0]) {
        int x = middle_x;
        int y = y1 + rng() % half_h;
        RemoveWall(cv::Point(x, y), cv::Point(x + 1, y));
    }
    if (inner_sides[1]) {
        int x = x1 + rng() % half_w;
        int y = middle_y;
        RemoveWall(cv::Point(x, y), cv::Point(x, y + 1));
    }
    if (inner_sides[2]) {
        int x = middle_x;
        int y = middle_y + 1 + rng() % half_h;
        RemoveWall(cv::Point(x, y), cv::Point(x + 1, y));
    }
    if (inner_sides[3]) {
        int x = middle_x + 1 + rng() % half_w;
        int y = middle_y;
        RemoveWall(cv::Point(x, y), cv::Point(x, y + 1));
    }
    recursion(x1, y1, middle_x, middle_y);
    recursion(middle_x + 1, y1, x2, middle_y);
    recursion(x1, middle_y + 1, middle_x, y2);
    recursion(middle_x + 1, middle_y + 1, x2, y2);
}

int main() {
    std::cout << "Maze width: ";
    std::cin >> width;
    std::cout << "Maze height: ";
    std::cin >> height;
    std::cout << "Maze cell size in pixels: ";
    std::cin >> cell_size;

    for (int x = 0; x < width; ++x) {
        std::vector<Cell> row;
        for (int y = 0; y < height; ++y) row.push_back(Cell());
        cells.push_back(row);
    }

    goal = cv::Point(width - 1, height - 1);
    start = cv::Point(0, 0);

    std::string algorithm;
    std::cout << "Algorithm to use [dfs/bfs/rec]: ";
    std::cin >> algorithm;

    if (algorithm == "dfs") {
        DFSMaze();
    } else if (algorithm == "bfs") {
        RandomBFSMaze();
    } else if (algorithm == "rec") {
        recursion(0, 0, width - 1, height - 1);
    } else {
        std::cout << "Invalid choice" << std::endl;
        return 1;
    }

    std::cout << std::endl;
    std::cout << "Creating image" << std::endl;
    draw();
    std::cout << "Image saved to output.png" << std::endl;
}
