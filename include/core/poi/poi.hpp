#ifndef THYME_ENVIRONMENTS_ROVERS_POI
#define THYME_ENVIRONMENTS_ROVERS_POI

#include <core/detail/pack.hpp>
#include <utilities/math/cartesian.hpp>

namespace rovers {

/*
 *
 * POI interface
 *
 */
class IPOI {
    using Point = thyme::math::Point;

   public:
    IPOI(double value, double obs_radius) : m_value(value), m_obs_radius(obs_radius) {}
    virtual ~IPOI() = default;

    const Point& position() const { return m_position; }
    void set_position(double x, double y) {
        m_position.x = x;
        m_position.y = y;
    }

    const double& value() const { return m_value; }
    const double& obs_radius() const { return m_obs_radius; }

    void set_observed(bool observed) { m_observed = observed; }
    const bool& observed() const { return m_observed; }

    void update() {
        // housekeeping.
        // delegate to tick for implementers.
        tick();
    }

    [[nodiscard]] virtual bool constraint_satisfied(const EntityPack&) const = 0;

   protected:
    virtual void tick() {}

   private:
    Point m_position;
    double m_value;

    double m_obs_radius;
    bool m_observed{false};
};

/*
 *
 * Default boilerplate poi
 *
 */
template <typename ConstraintPolicy>
class POI final : public IPOI {
   public:
    POI(double value = 1.0, double obs_radius = 1.0,
        ConstraintPolicy constraint = ConstraintPolicy())
        : IPOI(value, obs_radius), m_constraint(constraint) {}

    [[nodiscard]] bool constraint_satisfied(const EntityPack& entity_pack) const override {
        return m_constraint.is_satisfied(entity_pack);
    }

   private:
    ConstraintPolicy m_constraint;
};
}  // namespace rovers

#endif