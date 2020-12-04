#!/bin/bash
poetry run bash -c '

function run_py () {
    fname="$(basename -- $1)"
    line_n="${COLUMNS:-$(tput cols)}"
    mid=${#fname}
    others="${@:2}"
    othersn=${#others}
    wspace=${#@}
    text_len=$(( mid+othersn ))
    side=$(( line_n - text_len - wspace - 8 ))
    echo
    printf "[[[%*s "
    printf " $fname $others "
    printf " %*s\n" "${side}" "" | tr " " ] 

    python "$@"
}

run_py ./examples/simplest_example.py hello

run_py ./examples/script_example.py
run_py ./examples/script_example.py print-age
run_py ./examples/script_example.py print-name

run_py ./examples/traceback_example.py lumberjack

run_py ./examples/script_with_required_param_example.py
run_py ./examples/script_with_required_param_example.py print-age
run_py ./examples/script_with_required_param_example.py print-age
run_py ./examples/script_with_required_param_example.py print-age --age 12
run_py ./examples/script_with_required_param_example.py print-name
run_py ./examples/script_with_required_param_example.py print-name --name foo
run_py ./examples/script_with_required_param_example.py print-name foo

run_py ./examples/type_casting_example.py
run_py ./examples/type_casting_example.py run

run_py ./examples/config_example/my_curl.py headers
run_py ./examples/config_example/my_curl.py headers --url "https://oeksound.com"

cd examples

run_py -m advanced_module_example subcommand-foo
run_py -m advanced_module_example subcommand-foo --a B
run_py -m advanced_module_example subcommand-foo B 2 .
run_py -m advanced_module_example subcommand-bar

run_py -m module_example subcommand-foo
run_py -m module_example subcommand-bar
'
