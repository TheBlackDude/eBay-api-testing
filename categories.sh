#!/bin/bash
set -e

show_help() {
  echo """
  Commands
  ---------------------------------
  tests         : Run the tests
  --rebuild     : Download the data from the api and create the database
  --render      : Generate a html page with the given id's category
  """
}

case "$1" in
  "tests" )
    # run the tests
    python3 tests.py
  ;;
  "--rebuild" )
    # rebuild database
    python3 categories.py --rebuild
  ;;
  "--render" )
    # render post
    python3 categories.py --render "${@:2}"
  ;;
  * )
  show_help
  ;;
esac
