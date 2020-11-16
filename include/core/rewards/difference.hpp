#ifndef THYME_ENVIRONMENTS_ROVERS_DIFFERENCE
#define THYME_ENVIRONMENTS_ROVERS_DIFFERENCE

#include <core/rewards/global.hpp>
#include <utilities/ranges.hpp>

namespace rovers::rewards {

/*
 *
 * Difference between reward and the reward without the agent acting
 *
 */
class Difference {
   public:
    [[nodiscard]] double compute(const AgentPack& pack) const {
        double reward = Global().compute(pack);
        auto rovers_without_me = thyme::utilities::filter(
            pack.agents, [&](const auto& rover) { return &rover != &pack.agent; });
        double reward_without_me = Global().compute(pack);

        return reward - reward_without_me;
    }
};

}  // namespace rovers::rewards

#endif