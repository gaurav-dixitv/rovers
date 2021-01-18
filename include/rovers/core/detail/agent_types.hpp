#ifndef THYME_ENVIRONMENTS_ROVERS_ROVER_TYPES
#define THYME_ENVIRONMENTS_ROVERS_ROVER_TYPES

#include <rovers/utilities/shared_wrapper.hpp>

/*
*
* Agent abstraction
*
*/
namespace rovers {
class IRover;
using Agent = thyme::utilities::SharedWrap<IRover>;
}  // namespace rovers

#endif
