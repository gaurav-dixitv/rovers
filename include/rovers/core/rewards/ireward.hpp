#ifndef THYME_ENVIRONMENTS_ROVERS_IREWARD
#define THYME_ENVIRONMENTS_ROVERS_IREWARD

#include <rovers/core/detail/pack.hpp>

namespace rovers::rewards {

/*
 *
 * Reward interface for bindings
 *
 */
class IReward {
   public:
    [[nodiscard]] virtual double compute(const AgentPack&) const = 0;
    virtual ~IReward() = default;
};

}  // namespace rovers::rewards

#endif