#ifndef THYME_ENVIRONMENTS_ROVERS_GLOBAL
#define THYME_ENVIRONMENTS_ROVERS_GLOBAL

#include <rovers/core/detail/pack.hpp>

namespace rovers::rewards {

/*
 *
 * Default environment reward: checks if all constraints are satisfied
 *
 */
class Global {
   public:
    [[nodiscard]] double compute(const AgentPack& pack) const {
        // TODO pass in a view of POIContainer filtered by observed()
        // TODO Keep filtering over this view for speed-up
        double reward = 0.0;
        for (const auto& poi : pack.entities) {
            if (poi->observed()) continue;

            if (poi->constraint_satisfied({poi, pack.agents, pack.entities})) {
                poi->set_observed(true);  // TDDO emit signal to POI instead.
                reward += poi->value();
            }
        }
        return reward;
    }
};

}  // namespace rovers::rewards

#endif