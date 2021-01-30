#ifndef THYME_ENVIRONMENTS_ROVERS_ENVIRONMENT
#define THYME_ENVIRONMENTS_ROVERS_ENVIRONMENT

#include <Eigen/Dense>
#include <rovers/core/poi/count_constraint.hpp>
#include <rovers/core/poi/poi.hpp>
#include <rovers/core/poi/type_constraint.hpp>
#include <rovers/core/rover/rover.hpp>
#include <rovers/core/sensors/lidar.hpp>
#include <rovers/core/setup/init_random.hpp>
#include <rovers/utilities/spaces/discrete.hpp>
#include <tuple>
#include <vector>

namespace rovers {

/*
 *
 * Default Rovers environment
 *
 */
template <typename InitPolicy = RandomInit>
class Environment {
   public:
    using Action = Eigen::MatrixXd;
    using State = std::vector<Eigen::MatrixXd>;
    using Reward = std::vector<double>;

    Environment(InitPolicy initPolicy = InitPolicy(), std::vector<Agent> rovers = {},
                std::vector<Entity> pois = {}, size_t width = 10.0, size_t height = 10.0)
        : m_initPolicy(initPolicy),
          m_rovers(std::move(rovers)),
          m_pois(std::move(pois)),
          m_width(width),
          m_height(height) {}

    // helpers to set rovers/pois after the fact
    void set_rovers(std::vector<Agent> rovers) { m_rovers = std::move(rovers); }
    void set_pois(std::vector<Entity> pois) { m_pois = std::move(pois); }

    const std::vector<Agent>& rovers() { return m_rovers; }
    const std::vector<Entity>& pois() { return m_pois; }

    std::tuple<State, Reward> step(std::vector<Action> actions) {
        for (size_t i = 0; i < m_rovers.size(); ++i) {
            auto& rover = m_rovers[i];
            // call update for all rovers
            rover->update();
            // take actions
            rover->act(actions[i]);
            // bound position
            clamp_bounds(rover);
        }
        // call update for pois
        for (auto& poi : m_pois) poi->update();
        // return next observations and rewards
        return status();
    }

    std::tuple<State, Reward> reset() {
        // clear agents
        for (auto& r : m_rovers) r->reset();
        // reset pois
        for (auto& poi : m_pois) poi->set_observed(false);
        // initialize
        m_initPolicy.initialize(m_rovers, m_pois);
        // return next observations and rewards
        return status();
    }

    void render() {}
    void close() {}

    const size_t& width() { return m_width; }
    const size_t& height() { return m_height; }
    // TODO add pre/post update for all components

   private:
    inline void clamp_bounds(Agent& rover) {
        rover->set_position(std::clamp(rover->position().x, 0.0, 1.0 * m_width),
                            std::clamp(rover->position().y, 0.0, 1.0 * m_height));
    }

    std::tuple<State, Reward> status() {
        // observations and rewards
        State state;
        Reward rewards;
        for (auto& r : m_rovers) {
            state.push_back(r->scan({r, m_rovers, m_pois}));
            rewards.push_back(r->reward({r, m_rovers, m_pois}));
        }
        return {state, rewards};
    }

   private:
    InitPolicy m_initPolicy;
    std::vector<Agent> m_rovers;
    std::vector<Entity> m_pois;

    size_t m_width;
    size_t m_height;
};

/*
 *
 * Syntactic sugar for agents/entities
 *
 */
using Agents = std::vector<Agent>;
using Entities = std::vector<Entity>;
using Actions = std::vector<Eigen::MatrixXd>;

Eigen::MatrixXd tensor(std::vector<double> list) {
    return Eigen::Map<Eigen::MatrixXd>(list.data(), list.size(), 1);
}

Agents& operator<<(Agents& vector, Agent&& rover) {
    vector.push_back(std::move(rover));
    return vector;
}
Entities& operator<<(Entities& vector, Entity&& poi) {
    vector.push_back(std::move(poi));
    return vector;
}

}  // namespace rovers

#endif
