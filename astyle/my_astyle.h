/*
 * Copyright (C) dirlt
 */

#ifndef __CC_ASTYLE_MYASTYLE_H__
#define __CC_ASTYLE_MYASTYLE_H__

#include <string>

namespace astyle {

extern const char* kDefaultOptions;
const std::string my_astyle(const char* src,
                            const char* options = kDefaultOptions);

} // namespace astyle

#endif // __CC_ASTYLE_MYASTYLE_H__
