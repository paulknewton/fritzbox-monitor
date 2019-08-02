# Generate graphs and uploade to github.com
#

build_graph() {  # plotFunction title log_dir
    echo Building graphs for: $2
    git pull

    # generate the graphs
    python3 $1 stats --title "$2" --logdir "$3"

    # commit to git
    git add docs/*
    git commit -m "Updated $2 graphs"
    git push
}

# refresh code
git pull

# build graphs
build_graph fritz.py "Fritzbox 7530" logs.7530
