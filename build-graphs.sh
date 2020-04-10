#!/usr/bin/env bash
# Generate graphs and upload to github.com
#
#

build_graph() {  # plotFunction title log_dir prefix
    echo "Building graphs for: $2"

    # generate the graphs
    python3 "$1" stats --title "$2" --logdir "$3" --prefix "$4" --output docs

    # commit to git
    git add docs/*
    git commit -m "Updated $2 graphs"
    git push
}

# refresh code
git pull

# build graphs
build_graph fritz.py "Fritzbox 7390" logs.fritz7390 fritz7390
build_graph fritz.py "Fritzbox 7530" logs.fritz7530 fritz7530
