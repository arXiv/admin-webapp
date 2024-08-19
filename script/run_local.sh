#!/usr/bin/env bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
root_dir="$( dirname "$script_dir" )"

if [ ! -x poetry ] ; then
    # activate the venv if poetry not on the path yet
    source $root_dir/venv/bin/activate
fi
# Local run env
source $root_dir/.localenv
cat $root_dir/.localenv
echo ""
echo "Open"
echo "http://localhost.arxiv.org:5100/login"
echo ""

poetry run flask run --port 5100
