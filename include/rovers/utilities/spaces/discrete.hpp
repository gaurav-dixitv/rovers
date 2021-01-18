#ifndef THYME_SPACES_DISCRETE
#define THYME_SPACES_DISCRETE

#include <Eigen/Dense>
#include <random>

namespace thyme::spaces {

/*
 *
 * Partial Discrete space stub from thyme
 *
 */
class Discrete {
   public:
    using value_shape = Eigen::MatrixXd;
    using value_type = size_t;

    Discrete(std::size_t m = 1) : m_m(m) {
        std::random_device rd;
        m_gen = std::mt19937(rd());  // get global seed here
        m_dis = std::uniform_int_distribution<int>(0, m_m - 1);
    }
    value_type sample() { return m_dis(m_gen); }
    value_type max(const value_shape& values) {
        size_t max_index;
        values.col(0).maxCoeff(&max_index);
        return max_index;
    }

   private:
    std::size_t m_m;
    std::uniform_int_distribution<int> m_dis;
    std::mt19937 m_gen;
};

}  // namespace thyme::spaces

#endif