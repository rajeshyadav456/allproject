#!/usr/bin/env bash
# This script will setup the application stuffs like environment variables file depending upon the given environment.
# Arguments:
# 1. project directory (Absolute path of project root directory)
# 2. project environment (Default `development`)
set -eu

# Set magic variables for current file & dir
# shellcheck disable=SC2034
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC2034
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
# shellcheck disable=SC2034
__base="$(basename "${__file}" .sh)"

project_dir="${1}"
project_env="${2}"
project_env_file_path="${project_dir}/.env.${project_env}"
python_version="3.8.13"
pyenv_venv_name="soteria-backend-venv"
python_exec="python3"
system_user="$(id -u -n)"

setup_project_dir_permission() {
  sudo chown "${system_user}:${system_user}" -R "${project_dir}"
}

install_project_dependencies() {
  pushd "${project_dir}" || {
    echo "Not found directory: ${project_dir}"
    exit 1
  }

  # this we required for building 'psycopg2' package
  sudo apt install libpq-dev

  echo "Installing python project dependencies ..."
  pip install -r requirements.txt

  popd
}

do_db_migrations() {
  pushd "${project_dir}" || {
    echo "Not found directory: ${project_dir}"
    exit 1
  }
  echo "* Doing django db migrations"
  ${python_exec} manage.py migrate
  popd
}

collect_static_files() {
  pushd "${project_dir}" || {
    echo "Not found directory: ${project_dir}"
    exit 1
  }
  project_static_dir="$(sed -n 's/^STATIC_BASE_DIR="\(.*\)"$/\1/p' "${project_env_file_path}")"
  if [[ ! -d ${project_static_dir} ]]; then
    echo "Not found project static directory at ${project_static_dir}, creating it"
    sudo mkdir -p "${project_static_dir}"
    sudo chown "${system_user}":www-data "${project_static_dir}"
  fi

  echo "* Collecting fresh static files of django application"
  ${python_exec} manage.py collectstatic --noinput -c
  sudo chown "${system_user}":www-data -R "${project_static_dir}"
  popd
}

main() {
  # shellcheck source=scripts/_ensure.sh
  source "${__dir}/../_ensure.sh"

#  load_nvm
  load_pyenv

  # setup system directories needed for app running
  sudo tee /usr/lib/tmpfiles.d/soteria-backend.conf >/dev/null <<END
# Directory for temp/volatile files like pid files
d /var/run/soteria-backend 2775 ${system_user} ${system_user} - -
# Directory for data and libraries files
d /var/lib/soteria-backend 2775 ${system_user} ${system_user} - -
# Log directory
d /var/log/soteria-backend 1775 root ${system_user} - -
END

  sudo systemd-tmpfiles --create /usr/lib/tmpfiles.d/soteria-backend.conf

  setup_project_dir_permission
  ensure_pyenv_virtualenv "${python_version}" "${pyenv_venv_name}"
  activate_pyenv_virtualenv "${pyenv_venv_name}"
  install_project_dependencies
  do_db_migrations
  collect_static_files
  deactivate_pyenv_virtualenv "${pyenv_venv_name}"

}

main
