#ifndef THYME_MATH_NORMS
#define THYME_MATH_NORMS

#include <cmath>
#include <rovers/utilities/math/cartesian.hpp>

namespace thyme::math {

inline double l2_norm(const Point& a, const Point& b) {
    auto x = b.x - a.x;
    auto y = b.y - a.y;
    return sqrt(x * x + y * y);
}

inline std::pair<double, double> l2a(const Point& a, const Point& b) {
    auto angle = atan2(a, b) * to_degrees;
    auto distance = l2_norm(a, b);
    return {angle, distance};
}

}  // namespace thyme::math

#endif