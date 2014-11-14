/*
 * Copyright (C) dirlt
 */

#ifndef __CC_COMMON_LOGGER_INL_H__
#define __CC_COMMON_LOGGER_INL_H__

#include <cstdlib>
#include <cstdio>
#include <cerrno>
#include <cstring>

#define SERRNO (strerror(errno))
#define SERRNO2(n) (strerror(n))

namespace common {

enum log_level_t {
    T_DEBUG,
    T_NOTICE,
    T_TRACE,
    T_WARNING,
    T_FATAL
};
extern void set_log_level(log_level_t level);
extern log_level_t get_log_level();

extern void set_log_max_size(size_t size);
extern size_t get_log_max_size();

typedef void (*log_cb_t)(const char* msg);
extern void set_log_cb(log_cb_t cb);
extern log_cb_t get_log_cb();

extern void log_va(log_level_t level, const char* fmt, ...);
extern void log (log_level_t level, const char* msg);

} // namespace common

#ifndef NDEBUG
#define DEBUG(fmt,...)                                                  \
    (common::log_va(common::T_DEBUG,                                      \
                    "[%s][%s:%d]"fmt,                                     \
                    __FUNCTION__, __FILE__, __LINE__, ##__VA_ARGS__))
#else
#define DEBUG(fmt,...)
#endif

#define NOTICE(fmt,...)                                                 \
    (common::log_va(common::T_NOTICE,                                     \
                    "[%s][%s:%d]"fmt,                                     \
                    __FUNCTION__, __FILE__, __LINE__, ##__VA_ARGS__))
#define TRACE(fmt,...)                                              \
    (common::log_va(common::T_TRACE,                                  \
                    "[%s][%s:%d]"fmt,                                 \
                    __FUNCTION__, __FILE__, __LINE__, ##__VA_ARGS__))
#define WARNING(fmt,...)                                            \
    (common::log_va(common::T_WARNING,                                \
                    "[%s][%s:%d]"fmt,                                 \
                    __FUNCTION__, __FILE__, __LINE__, ##__VA_ARGS__))
#define FATAL(fmt,...)                                                  \
    (common::log_va(common::T_FATAL,                                    \
                    "[%s][%s:%d]"fmt,                                     \
                    __FUNCTION__, __FILE__, __LINE__, ##__VA_ARGS__))

#endif // __CC_COMMON_LOGGER_INL_H__
