#ifndef THYME_UTILITIES_SHARED_WRAPPER
#define THYME_UTILITIES_SHARED_WRAPPER

#include <memory>

namespace thyme::utilities {

/*
 *
 * Wrapped shared pointer for memory management/profiling.
 * Modified from thyme::utilities::UniqueWrap for the python binding prototype
 *
 */
template <typename T>
class SharedWrap {
   public:
    template <typename U>
    SharedWrap(U x) : self_(std::make_shared<U>(std::move(x))) {}

    SharedWrap(const SharedWrap& x) = default;
    SharedWrap(SharedWrap&&) noexcept = default;
    ~SharedWrap() = default;

    SharedWrap& operator=(const SharedWrap& x) {
        SharedWrap tmp(x);
        *this = std::move(tmp);
        return *this;
    }
    SharedWrap& operator=(SharedWrap&& x) noexcept = default;
    T* operator->() const { return self_.get(); }

   public:
    std::shared_ptr<T> self_;
};

}  // namespace thyme::utilities

#endif