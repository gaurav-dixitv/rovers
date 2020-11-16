#ifndef THYME_MATH_CARTESIAN
#define THYME_MATH_CARTESIAN

#include <cmath>
#include <ostream>

namespace thyme::math {

inline static constexpr double to_degrees = 180.0 / M_PI;
inline static constexpr double two_pi = 2 * M_PI;

struct Point {
    double x;
    double y;
    Point(double x = 0.0, double y = 0.0) : x(x), y(y) {}
};
std::ostream& operator<<(std::ostream& os, const Point& point) {
    os << "[" << point.x << "," << point.y << "]" << std::endl;
    return os;
}

inline double atan2(const Point& a, const Point& b) {
    auto x = b.x - a.x;
    auto y = b.y - a.y;
    double angle = ::atan2(x, y);
    return angle >= 0 ? angle : angle + two_pi;
}

}  // namespace thyme::math

#endif