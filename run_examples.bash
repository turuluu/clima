#!/bin/bash
set -x
poetry run python ./examples/simplest_example.py hello

poetry run python ./examples/script_example.py
poetry run python ./examples/script_example.py print-age
poetry run python ./examples/script_example.py print-name

echo "The next example demonstrates the error output"
poetry run python ./examples/traceback_example.py lumberjack

poetry run python ./examples/script_with_required_param_example.py
poetry run python ./examples/script_with_required_param_example.py print-age
poetry run python ./examples/script_with_required_param_example.py print-age
poetry run python ./examples/script_with_required_param_example.py print-age --age 12
poetry run python ./examples/script_with_required_param_example.py print-name
poetry run python ./examples/script_with_required_param_example.py print-name --name foo
poetry run python ./examples/script_with_required_param_example.py print-name foo

poetry run python ./examples/type_casting_example.py
poetry run python ./examples/type_casting_example.py run

poetry run python ./examples/config_example/my_curl.py headers
poetry run python ./examples/config_example/my_curl.py headers --url 'https://oeksound.com'

poetry run bash -c 'cd examples; python -m advanced_module_example subcommand-foo'
poetry run bash -c 'cd examples; python -m advanced_module_example subcommand-foo -a B'
poetry run bash -c 'cd examples; python -m advanced_module_example subcommand-foo B 2 .'
poetry run bash -c 'cd examples; python -m advanced_module_example subcommand-bar'

poetry run bash -c 'cd examples; python -m module_example subcommand-foo'
poetry run bash -c 'cd examples; python -m module_example subcommand-bar'

