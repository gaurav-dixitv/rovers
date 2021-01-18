#ifndef THYME_ENVIRONMENTS_ROVERS_ISENSOR
#define THYME_ENVIRONMENTS_ROVERS_ISENSOR

#include <Eigen/Dense>
#include <rovers/core/detail/pack.hpp>

namespace rovers {

/*
 *
 * sensor interface for bindings
 *
 */
class ISensor {
   public:
    [[nodiscard]] virtual Eigen::MatrixXd scan(const AgentPack& pack) const = 0;
    virtual ~ISensor() = default;
};

}  // namespace rovers
#endif