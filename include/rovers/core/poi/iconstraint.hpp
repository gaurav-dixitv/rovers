#ifndef THYME_ENVIRONMENTS_ROVERS_POI_ICONSTRAINT
#define THYME_ENVIRONMENTS_ROVERS_POI_ICONSTRAINT

#include <rovers/core/detail/pack.hpp>

namespace rovers {

/*
 *
 * Constraint interface for bindings
 *
 */
class IConstraint {
   public:
    [[nodiscard]] virtual bool is_satisfied(const EntityPack& entity_pack) const = 0;
    virtual ~IConstraint() = default;
};

}  // namespace rovers

#endif