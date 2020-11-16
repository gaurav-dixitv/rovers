#ifndef THYME_UTILITIES_IDENTITY
#define THYME_UTILITIES_IDENTITY

#include <variant>

namespace thyme::utilities {

template <typename T>
inline bool is_identity(const T& t, const T& u) {
    return std::addressof(t) == std::addressof(u);
}

template <typename T, class... Types>
inline bool is_identity(const T& t, const std::variant<Types...>& v) {
    if (const T* c = std::get_if<T>(&v))
        return is_identity(*c, t);
    else
        return false;
}
template <typename T, class... Types>
inline bool is_identity(const std::variant<Types...>& v, const T& t) {
    return is_identity(t, v);
}

}  // namespace thyme::utilities

#endif
