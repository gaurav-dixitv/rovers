#ifndef THYME_ENVIRONMENTS_ROVERS_INIT_CORNERS
#define THYME_ENVIRONMENTS_ROVERS_INIT_CORNERS

#include <cmath>
// #include <ranges>

namespace rovers {

/*
 *
 * agent/entity initialization policy for corner initialization
 *
 */
class CornersInit {
   public:
    CornersInit(double span = 10.0) : m_span(span) {}

    // template <std::ranges::range RoverContainer, std::ranges::range POIContainer>
    template <typename RoverContainer, typename POIContainer>
    void initialize(RoverContainer& rovers, POIContainer& pois) {
        initialize_rovers(rovers);
        initialize_poi(pois);
    }

   private:
    // template <std::ranges::range RoverContainer>
    template <typename RoverContainer>
    void initialize_rovers(RoverContainer& rovers) {
        const double start = 1.0;
        const double end = m_span - 1.0;
        const int rad = int(m_span / sqrt(3) / 2.0);
        const int center = int((start + end) / 2.0);
        double x, y;
        for (std::size_t i = 0; i < rovers.size(); ++i) {
            unsigned quadrant = i % 4;
            if (quadrant == 0) {
                x = center - 1 - std::fmod(i / 4.0, center - rad);
                y = center - std::fmod(i / (4.0 * center - rad), center - rad);
            } else if (quadrant == 1) {
                x = center + std::fmod(i / (4.0 * center - rad), center - rad) - 1;
                y = center - 1 + std::fmod(i / 4.0, center - rad);
            } else if (quadrant == 2) {
                x = center + 1 + std::fmod(i / 4.0, center - rad);
                y = center + std::fmod(i / (4.0 * center - rad), center - rad);
            } else {
                x = center - std::fmod(i / (4.0 * center - rad), center - rad);
                y = center + 1 - std::fmod(i / 4.0, center - rad);
            }
            rovers[i]->set_position(x, y);
        }
    }
    // template <std::ranges::range POIContainer>
    template <typename POIContainer>
    void initialize_poi(POIContainer& pois) {
        pois.size();
        const double start = 0.0;
        const double end = m_span - 1.0;
        double x, y;
        for (std::size_t i = 0; i < pois.size(); ++i) {
            if (i % 4 == 0) {
                x = start + int(i / 4);
                y = start + int(i / 3);
            } else if (i % 4 == 1) {
                x = end - int(i / 4);
                y = start + int(i / 4);
            } else if (i % 4 == 2) {
                x = start + int(i / 4);
                y = end - int(i / 4);
            } else {
                x = end - int(i / 4);
                y = end - int(i / 4);
            }
            pois[i]->set_position(x, y);
        }
    }

   private:
    double m_span;
};
}  // namespace rovers

#endif
