#ifndef THYME_ENVIRONMENTS_ROVERS_LIDAR
#define THYME_ENVIRONMENTS_ROVERS_LIDAR

#include <Eigen/Dense>
#include <numeric>
#include <rovers/core/detail/pack.hpp>
#include <rovers/core/poi/poi.hpp>
#include <rovers/core/rover/rover.hpp>
#include <rovers/utilities/math/norms.hpp>
// #include <ranges> // changed for python branch
#include <vector>

namespace rovers {

/*
 *
 * Lidar composition strategies
 *
 */
class Density {
   public:
    // template <std::ranges::range Range, typename Tp, typename Up>
    template <typename Range, typename Tp, typename Up>
    inline Tp compose(const Range& range, Tp init, Up scale) const {
        return std::accumulate(std::begin(range), std::end(range), init) / scale;
    }
};

class Closest {
   public:
    // template <std::ranges::range Range, typename Tp, typename Up>
    template <typename Range, typename Tp, typename Up>
    inline Tp compose(const Range& range, Tp, Up) const {
        return *std::max_element(std::begin(range), std::end(range));
    }
};

/*
 *
 *  composition strategy interface for bindings
 *
 */
class ISensorComposition {
   public:
    virtual inline double compose(const std::vector<double>, double, double) = 0;
    virtual ~ISensorComposition() = default;
};

/*
 *
 * Lidar
 *
 */
template <typename CompositionPolicy = Density>
class Lidar {
    using CPolicy = thyme::utilities::SharedWrap<CompositionPolicy>;

   public:
    Lidar(double resolution = 90, CPolicy composition_policy = CompositionPolicy())
        : m_resolution(resolution), m_composition(composition_policy) {}

    [[nodiscard]] Eigen::MatrixXd scan(const AgentPack& pack) const {
        const std::size_t num_sectors = 360 / m_resolution;
        std::vector<std::vector<double>> poi_values(num_sectors), rover_values(num_sectors);
        auto& rover = pack.agent;  // convenient handle

        // observe pois
        for (const auto& sensed_poi : pack.entities) {
            if (sensed_poi->observed()) continue;
            auto [angle, distance] = thyme::math::l2a(rover->position(), sensed_poi->position());
            if (distance > rover->obs_radius()) continue;

            int sector = angle / m_resolution;
            poi_values[sector].push_back(sensed_poi->value() /
                                         std::max(0.001, distance * distance));
        }

        // observe rovers
        for (const auto& sensed_rover : pack.agents) {
            if (&sensed_rover == &rover) continue;

            auto [angle, distance] = thyme::math::l2a(rover->position(), sensed_rover->position());
            if (distance > rover->obs_radius()) continue;

            int sector = angle / m_resolution;
            rover_values[sector].push_back(1.0 / std::max(0.001, distance * distance));
        }

        // encode state
        Eigen::MatrixXd state(num_sectors * 2, 1);

        for (std::size_t i = 0; i < num_sectors; ++i) {
            const std::size_t& num_rovers = rover_values[i].size();
            const std::size_t& num_poi = poi_values[i].size();
            state(i) = state(num_sectors + i) = -1.0;

            if (num_rovers > 0) state(i) = m_composition->compose(rover_values[i], 0.0, num_rovers);
            if (num_poi > 0)
                state(num_sectors + i) = m_composition->compose(poi_values[i], 0.0, num_poi);
        }
        return state;
    }

   private:
    double m_resolution;
    CPolicy m_composition;
};
}  // namespace rovers

#endif