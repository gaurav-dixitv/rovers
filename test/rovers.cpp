
#include <iostream>
#include <rovers/core/poi/type_constraint.hpp>
#include <rovers/core/rewards/difference.hpp>
#include <rovers/core/setup/init_corners.hpp>
#include <rovers/environment.hpp>
#include <rovers/utilities/spaces/discrete.hpp>

int main() {
    using namespace rovers;

    using Dense = Lidar<Density>;
    using Close = Lidar<Closest>;
    using Discreet = thyme::spaces::Discrete;

    // creating lists with Qt style syntactic sugar
    Agents rovers;
    // create agent with lidar, discrete action space and difference reward:
    rovers << Rover<Close, Discreet, rewards::Difference>(2.0, Close(45));
    // Defaults to global/env reward when not specified. Create two rovers with dense lidars and
    // global reward:
    rovers << Rover<Dense, Discreet>(1.0, Dense(90)) << Rover<Dense, Discreet>(3.0, Dense(90));
    // a flying drone!
    rovers << Drone();

    // or without the << sugar. Three POIs with Count and Type constraints:
    Entities pois = {POI<CountConstraint>(3), POI<TypeConstraint>(2, 1.0), POI<TypeConstraint>(5)};

    // Environment with rovers and pois placed in the corners. Defaults to random initialization if
    // unspecified.
    using Env = Environment<CornersInit>;
    // Create an environment with our rovers and pois:
    auto env = Env(CornersInit(10.0), rovers, pois);
    env.reset();

    Actions actions;
    for (size_t i = 0; i < rovers.size(); ++i) {
        actions.emplace_back(Eigen::Vector2d::Random());  // random dx, dy
    }
    auto [states, rewards] = env.step(actions);
    // print sample state
    std::cout << "\nSample environment state (each row corresponds to the state of a rover): "
              << std::endl;
    for (const auto& state : states) {
        std::cout << state.transpose() << std::endl;
    }

    /*
    using space = Discreet;
    using policy = thyme::rl::policies::PPO<space>;
    ..
    ..
    ..
    */

    return 0;
}