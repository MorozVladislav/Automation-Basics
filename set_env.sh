#!/usr/bin/env bash

source <(sed -E -n 's/[^#]+/export &/ p' $1)