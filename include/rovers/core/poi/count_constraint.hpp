#ifndef THYME_ENVIRONMENTS_ROVERS_POI_COUNT_CONSTRAINT
#define THYME_ENVIRONMENTS_ROVERS_POI_COUNT_CONSTRAINT

#include <rovers/core/poi/poi.hpp>
#include <rovers/core/rover/rover.hpp>

namespace rovers {

/*
 *
 * Constraint satifisted by a count of observations
 *
 */
class CountConstraint {
   public:
    CountConstraint(size_t count = 3) : count_constraint(count) {}

    [[nodiscard]] bool is_satisfied(const EntityPack& entity_pack) const {
        size_t count = 0;
        for (const auto& rover : entity_pack.agents) {
            if (rover->obs_radius() <= entity_pack.entity->obs_radius()) {
                ++count;
                if (count >= count_constraint) return true;
            }
        }
        return false;
    }

   private:
    size_t count_constraint;
};

}  // namespace rovers

#endif