#ifndef THYME_ENVIRONMENTS_ROVERS_POI_TYPES
#define THYME_ENVIRONMENTS_ROVERS_POI_TYPES

#include <rovers/utilities/shared_wrapper.hpp>

/*
 *
 * Entity abstraction
 *
 */
namespace rovers {
class IPOI;
using Entity = thyme::utilities::SharedWrap<IPOI>;
}  // namespace rovers

#endif
