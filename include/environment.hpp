#ifndef THYME_ENVIRONMENTS_ROVERS_ENVIRONMENT
#define THYME_ENVIRONMENTS_ROVERS_ENVIRONMENT

#include <Eigen/Dense>
#include <core/poi/count_constraint.hpp>
#include <core/poi/poi.hpp>
#include <core/poi/type_constraint.hpp>
#include <core/rover/rover.hpp>
#include <core/sensors/lidar.hpp>
#include <core/setup/init_random.hpp>
#include <tuple>
#include <utilities/spaces/discrete.hpp>
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
    using Action = size_t;
    using State = std::vector<Eigen::MatrixXd>;
    using Reward = std::vector<double>;

    Environment(InitPolicy initPolicy = InitPolicy(), std::vector<Agent> rovers = {},
                std::vector<Entity> pois = {})
        : m_initPolicy(initPolicy), m_rovers(std::move(rovers)), m_pois(std::move(pois)) {}

    // helpers to set rovers/pois after the fact
    void set_rovers(std::vector<Agent> rovers) { m_rovers = std::move(rovers); }
    void set_pois(std::vector<Entity> pois) { m_pois = std::move(pois); }

    std::tuple<State, Reward> step(std::vector<Action> actions) {
        for (size_t i = 0; i < m_rovers.size(); ++i) {
            auto& rover = m_rovers[i];
            // call update for all rovers
            rover->update();
            // take actions
            rover->apply_action(actions[i]);
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

    // TODO add pre/post update for all components

   private:
    inline void clamp_bounds(Agent& rover) {
        rover->set_position(std::clamp(rover->position().x, 0.0, 10.0),
                            std::clamp(rover->position().y, 0.0, 10.0));
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
};

/*
 *
 * Syntactic sugar for agents/entities
 *
 */
using Agents = std::vector<Agent>;
using Entities = std::vector<Entity>;
using Actions = std::vector<size_t>;

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