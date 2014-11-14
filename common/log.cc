/*
 * Copyright (C) dirlt
 */

#include <cstdarg>
#include "log.h"

namespace common {

static void default_log_cb(const char* msg) {
    fprintf(stderr, "%s", msg);
}

static log_cb_t log_cb = default_log_cb;
static log_level_t log_level = T_DEBUG;
static size_t log_max_size = 2048;

void set_log_level(log_level_t level) {
    log_level = level;
}
log_level_t get_log_level() {
    return log_level;
}

void set_log_max_size(size_t size) {
    log_max_size = size;
}
size_t get_log_max_size() {
    return log_max_size;
}

void set_log_cb(log_cb_t cb) {
    log_cb = cb ;
}
log_cb_t get_log_cb() {
    return log_cb;
}

static const char* log_level_srep[] = {
    "DEBUG", "NOTICE", "TRACE", "WARNING", "FATAL"
};

void log_va(log_level_t level, const char* fmt, ...) {
    char* msg = static_cast<char*>(alloca(log_max_size));
    size_t offset = 0;
    offset += snprintf(msg, log_max_size - offset, "[%s]", log_level_srep[level]);
    va_list ap;
    va_start(ap, fmt);
    offset += vsnprintf(msg + offset, log_max_size - offset, fmt, ap);
    va_end(ap);
    offset += snprintf(msg + offset, log_max_size - offset, "%s", "\n");
    log_cb(msg);
}

void log(log_level_t level, const char* msg) {
    char* buf = static_cast<char*>(alloca(log_max_size));
    snprintf(buf, log_max_size, "[%s]%s\n", log_level_srep[level], msg);
    log_cb(buf);
}

} // namespace common
