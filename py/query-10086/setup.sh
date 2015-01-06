#!/usr/bin/env bash
#Copyright (C) dirlt

mkdir -p att
cat schema | sqlite3 input.db
