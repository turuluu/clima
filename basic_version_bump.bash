#!/bin/bash

read -r -p "version bump (patch)? [Y/n]" response
response=${response,,} # tolower
if [[ $response =~ ^(yes|y| ) ]] || [[ -z $response ]]; then
	poetry version patch
fi

read -r -p "git add and commit? [Y/n]" response
response=${response,,} # tolower
if [[ $response =~ ^(yes|y| ) ]] || [[ -z $response ]]; then
	git add -p .
	git commit
fi

read -r -p "build and publish? [Y/n]" response
response=${response,,} # tolower
if [[ $response =~ ^(yes|y| ) ]] || [[ -z $response ]]; then
	poetry build
	poetry publish
fi

echo "Done!"
