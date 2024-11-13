#!/bin/bash

# Options are { major, minor, patch }
# see poetry version -h
version_flavour="${1:-patch}"

function query () {
    read -r -p "${*:1}? [Y/n] " response
    local response=$( echo $response | tr '[:upper:]' '[:lower:]' | cut -c1 )
    if [[ $response =~ y ]] || [[ -z $response ]]; then
        echo y
    fi
}

function check_poetry_installation () {
    if ! poetry >/dev/null 2>&1; then
        echo "python-poetry not installed. Install for example:"
        echo "   curl -sSL https://install.python-poetry.org | python3 -"
        echo "" 
        echo "Check the website for installation instructions:"
        echo "https://python-poetry.org/docs/master/#installing-with-the-official-installer"
        echo ""
        echo "Aborting.."
        exit 1
    fi
}

function main () {
    step="version bump ($version_flavour)" 
    if [[ $( query $step ) == y ]]; then
        check_poetry_installation
        poetry version $version_flavour
    fi

    step="git add and commit" 
    if [[ $( query $step ) == y ]]; then
        git add -p .
        git commit
    fi

    step="build"
    if [[ $( query $step ) == y ]]; then
        check_poetry_installation
        poetry build
    fi

    step="git push"
    if [[ $( query $step ) == y ]]; then
        git push
    fi

    step="Install locally"
    if [[ $( query $step ) == y ]]; then
        check_poetry_installation
        package="$( poetry env info -p 2>&1| cut -d'/' -f 8 | rev | cut -d'-' -f3- | rev | tr '-' '_' )"
        version="$( poetry version -s )"
        whl="$( ls -1 dist/$package-$version-*.whl 2>&1 )"

        echo "uninstalling $package"
        pip uninstall "$package"
        echo "installing from $whl"
        pip install "$whl"
    fi
}

main 2>&1
echo "Done!"
exit 0
