#ifndef THYME_ENVIRONMENTS_ROVERS_POI_TYPE_CONSTRAINT
#define THYME_ENVIRONMENTS_ROVERS_POI_TYPE_CONSTRAINT

#include <core/poi/poi.hpp>
#include <core/rover/rover.hpp>

namespace rovers {

/*
 *
 * Constraint satisfied by agents of a types observing together
 *
 */
class TypeConstraint {
   public:
    TypeConstraint(size_t count = 3) : count_constraint(count) {}

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
