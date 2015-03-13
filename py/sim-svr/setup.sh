#!/usr/bin/env bash
#Copyright (C) dirlt

mkdir -p static
cat schema | sqlite3 phone-book.db

