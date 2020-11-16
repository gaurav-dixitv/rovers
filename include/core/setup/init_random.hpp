#ifndef THYME_ENVIRONMENTS_ROVERS_INIT_RANDOM
#define THYME_ENVIRONMENTS_ROVERS_INIT_RANDOM

namespace rovers {

/*
 *
 * Random agent/entity initialization stub
 *
 */
class RandomInit {
   public:
    RandomInit() = default;

    template <typename RoverContainer, typename POIContainer>
    void initialize(RoverContainer& rovers, POIContainer& pois) {
        initialize_rovers(rovers);
        initialize_poi(pois);
    }

   private:
    template <typename RoverContainer>
    void initialize_rovers(RoverContainer& rovers) {
        for (std::size_t i = 0; i < rovers.size(); ++i) {
            rovers[i].position = {0.0, 0.0};
        }
    }
    template <typename POIContainer>
    void initialize_poi(POIContainer& pois) {
        for (std::size_t i = 0; i < pois.size(); ++i) {
            pois[i].position = {0.0, 0.0};
        }
    }
};
}  // namespace thyme::environments::rovers

#endif