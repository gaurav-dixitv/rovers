#ifndef THYME_UTILITIES_RANGES
#define THYME_UTILITIES_RANGES

namespace thyme::utilities {

template <typename Container, typename Predicate>
Container filter(const Container &container, Predicate predicate) {
    Container result;
    std::copy_if(container.begin(), container.end(), std::back_inserter(result), predicate);
    return result;
}

}  // namespace thyme::utilities

#endif