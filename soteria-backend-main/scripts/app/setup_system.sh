#!/usr/bin/env bash
# This script will install system level dependencies required for application setup and running.
set -eu

# Set magic variables for current file & dir
# shellcheck disable=SC2034
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC2034
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
# shellcheck disable=SC2034
__base="$(basename "${__file}" .sh)"

PYTHON_VERSION="3.8.13"
NODE_VERSION="14.19.1"
PM2_VERSION="5.2.0"

main() {
  echo "* Updating system..."
  sudo apt-get -y update

  # shellcheck source=scripts/_ensure.sh
  source "${__dir}/../_ensure.sh"

  ensure_pyenv
  ensure_python_version "${PYTHON_VERSION}"
  ensure_jq
  ensure_nvm
  ensure_node "${NODE_VERSION}"
  ensure_pm2 "${PM2_VERSION}"

}

main
