#!/usr/bin/env bash
# This file must be used sourced
# you cannot run it directly

if [ "${BASH_SOURCE-}" = "$0" ]; then
  echo "You must source this script: \$ source $0" >&2
  exit 33
fi

ensure_python_build_dependencies() {
  # pyenv build python from source code while installing it, so we have to ensure
  # that our system has all suitable dependencies to build necessary modules.
  # https://devguide.python.org/setup/#install-dependencies
  sudo apt-get install -y build-essential gdb lcov libbz2-dev libffi-dev \
    libgdbm-dev liblzma-dev libncurses5-dev libreadline6-dev \
    libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev
}

_load_pyenv() {
  #  Assume, pyenv is installed, it will update necessary environment variables and
  #  do basic initialization of pyenv
  eval "$(pyenv init --path)"
  eval "$(pyenv init -)"
  echo "Pyenv loading done"
}

load_pyenv() {
  # if pyenv not loaded, then load it
  # shellcheck disable=SC2015
  [[ ! -x "$(command -v pyenv)" ]] && _load_pyenv || echo "Pyenv already loaded"
}

ensure_pyenv() {
  # Assume, pyenv should be installed at current user home directory
  if [[ -d "${HOME}/.pyenv" ]]; then
    echo "* 'pyenv' is installed at '${HOME}/.pyenv'"
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
  else
    echo "WARN: pyenv is not installed at '${HOME}/.pyenv'"
    echo "Installing pyenv ..."
    curl https://pyenv.run | bash
    echo "Loading pyenv into shell ..."
  fi

  load_pyenv
}

ensure_python_version() {
  local python_version="${1}"
  if (pyenv versions --bare | grep -q "^${python_version}$"); then
    echo "* 'python(${python_version})' is installed"
  else
    echo "WARN: python version ${python_version} is not installed"
    echo "Installing python system level build dependencies ..."
    ensure_python_build_dependencies
    echo "Installing python version ${python_version} ..."
    pyenv install -s "${python_version}"
  fi
}

ensure_pyenv_virtualenv() {
  local python_version="${1}"
  local pyenv_venv_name="${2}"

  load_pyenv

  if (pyenv virtualenvs --bare | grep  -q "^${pyenv_venv_name}$"); then
    echo "Already found pyenv virtual environment '${pyenv_venv_name}'"
  else
    echo "Creating pyenv virtual environment '${pyenv_venv_name}' ..."
    pyenv virtualenv "${python_version}" "${pyenv_venv_name}"
  fi
}

activate_pyenv_virtualenv() {
  local pyenv_venv_name="${1}"

  load_pyenv

  echo "* Activating pyenv virtual environment '${pyenv_venv_name}'"
  eval "$(PYENV_VIRTUALENV_DISABLE_PROMPT=1 pyenv sh-activate "${pyenv_venv_name}")"
  echo "$(python --version) is available"

}


deactivate_pyenv_virtualenv() {
  local pyenv_venv_name="${1}"

  load_pyenv

  echo "* Deactivating pyenv virtual environment '${pyenv_venv_name}'"
  eval "$(pyenv sh-deactivate)"
}


ensure_jq() {
  if ! [[ -x "$(command -v jq)" ]]; then
    echo "WARN: 'jq' is not installed." >&2
    echo "Installing jq ..."
    sudo apt-get install jq -yqq
  else
    echo "* 'jq' tool is already installed"
  fi
}

_load_nvm() {
  # we have to load nvm now, otherwise other tools will not detect it
  export NVM_DIR="$HOME/.nvm"
  #  shellcheck disable=SC1090
  [[ -s "$NVM_DIR/nvm.sh" ]] && \. "$NVM_DIR/nvm.sh" # This loads nvm
}

load_nvm() {
  # if nvm not loaded, then load it
  # shellcheck disable=SC2015
  [[ ! -x "$(command -v nvm)" ]] && _load_nvm || true
}

ensure_nvm() {
  if ! [[ -d "$HOME/.nvm" ]]; then
    echo "WARN: 'nvm' is not installed." >&2
    echo "Installing nvm ..."
    wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
  else
    echo "* 'nvm' tool is already installed at '$HOME/.nvm'"
  fi

  load_nvm
}

ensure_node() {
  local node_version="${1}"

  load_nvm

  if (nvm ls "${node_version}" > /dev/null); then
    echo "* 'node'(${node_version}) is already installed"
  else
    echo "WARN: 'node(${node_version})' is not installed." >&2
    echo "Installing node(${node_version}) ..."
    nvm install "${node_version}"
    nvm use "${node_version}"
  fi
}

ensure_pm2() {
  local pm2_version="${1}"

  load_nvm

  if ! [[ -x "$(command -v pm2)" ]]; then
    echo "WARN: 'pm2' is not installed." >&2
    echo "Installing pm2 ..."
    npm install -g "pm2@${pm2_version}"
  else
    echo "* 'pm2' tool is already installed"
  fi
}

ensure_wkhtmltopdf() {
  if ! [[ -x "$(command -v wkhtmltopdf)" ]]; then
    echo "WARN: 'wkhtmltopdf' is not installed." >&2
    echo "Installing wkhtmltopdf and wkhtmltoimage for html rendering ..."
    # we are installing this package from official website, because we need patched qt based package version.
    wget -O "wkhtmltox_0.12.6-1.deb" \
      "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.$(lsb_release -cs)_amd64.deb"

    # dependencies of this package
    sudo apt install xfonts-75dpi

    sudo dpkg -i "wkhtmltox_0.12.6-1.deb"
    rm -rf "wkhtmltox_0.12.6-1.deb"
  else
    echo "* 'wkhtmltopdf' tool is already installed"
  fi
}
