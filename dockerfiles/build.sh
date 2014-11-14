#!/usr/bin/env bash
#Copyright (C) dirlt

build_base() {
    docker build -t tomb/ubuntu:base base
}
build_mysql() {
    build_base
    docker build -t tomb/ubuntu:mysql mysql
}
build_redis() {
    build_base
    docker build -t tomb/ubuntu:redis redis
}

cmd=${1:-"base"}
case $1 in 
    base)
        build_base
        ;;
    mysql)
        build_mysql
        ;;
    redis)
        build_redis
        ;;
    *)
        build_base
esac

