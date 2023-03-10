#!/usr/bin/env bash
set -e

# Set magic variables for current file & dir
# shellcheck disable=SC2034
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC2034
project_root=$(readlink -f "${__dir}/../")

pushd "${project_root}" > /dev/null
poetry export -f requirements.txt --without-hashes -o requirements.txt
poetry export -f requirements.txt --without-hashes --dev -o requirements-dev.txt
popd > /dev/null
