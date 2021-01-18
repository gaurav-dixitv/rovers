#ifndef THYME_MATH_RANDOM
#define THYME_MATH_RANDOM

#include <cmath>
#include <random>

namespace thyme::math {

std::mt19937 rand_gen;
std::uniform_real_distribution<> rand_uniform_dist(0.0, 1.0);
std::normal_distribution<> rand_normal_dist(0.0, 1.0);

inline double random() { return rand_uniform_dist(rand_gen); }

inline double random(const double lo, const double hi) {
    return lo + (hi - lo) * rand_uniform_dist(rand_gen);
}

inline double rand_bernoulli(const double input) {
    if (random() < input)
        return 1;
    else
        return 0;
}

inline int rand_int(const int hi_exclusive) {
    return (int)std::floor((double)hi_exclusive * rand_uniform_dist(rand_gen));
}

inline int rand_int(const int lo, const int hi_exclusive) {
    return lo + (int)std::floor((double)(hi_exclusive - lo) * rand_uniform_dist(rand_gen));
}

inline double rand_normal() { return rand_normal_dist(rand_gen); }

inline double rand_normal(const double mean, const double variance) {
    return variance * rand_normal_dist(rand_gen) + mean;
}

}  // namespace thyme::math

#endif