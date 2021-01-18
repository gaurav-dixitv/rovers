#ifndef THYME_UTILITIES_VISITOR
#define THYME_UTILITIES_VISITOR

#include <variant>

namespace thyme::utilities {

// TODO Add parameter pack support.
/*
 *
 * Minimal stub interface from thyme:: for the python binding prototype
 *
 */
template <typename T, class... Types>
inline auto apply_visitor(T t, std::variant<Types...>& v) {
    return t(v);
}

template <typename T, class... Types>
inline auto apply_visitor(T t, const std::variant<Types...>& v) {
    return t(v);
}

}  // namespace thyme::utilities

#endif