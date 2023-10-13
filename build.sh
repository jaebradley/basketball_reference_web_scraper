#!/bin/bash

function main() {
  local -r current_directory=$(pwd)
  if [[ "0" != "$?" ]]; then printf "Cannot identify current working directory\n" && exit 255; fi

  local -r dependencies_folder_path="${current_directory}/dependencies"

  mkdir -p "${dependencies_folder_path}"
  if [[ "0" != "$?" ]]; then printf "Creating dependencies folder at ${dependencies_folder_path} failed\n" && exit 255; fi

  command -v "python3"
  if [[ "0" != "$?" ]]; then printf "Cannot identify python3 program\n" && exit 255; fi

<<'###POETRY_INSTALLATION_DOCUMENTATION'
  From https://python-poetry.org/docs/#installing-manually;

  "Poetry can be installed manually using pip and the venv module. By doing so you will essentially perform the steps carried out by the official installer. As this is an advanced installation method, these instructions are Unix-only and omit specific examples such as installing from git.

  The variable $VENV_PATH will be used to indicate the path at which the virtual environment was created.

  python3 -m venv $VENV_PATH
  $VENV_PATH/bin/pip install -U pip setuptools
  $VENV_PATH/bin/pip install poetry

  Poetry will be available at $VENV_PATH/bin/poetry and can be invoked directly or symlinked elsewhere.

  To uninstall Poetry, simply delete the entire $VENV_PATH directory."
###POETRY_INSTALLATION_DOCUMENTATION

  python3 -m venv "${dependencies_folder_path}"
  if [[ "0" != "$?" ]]; then printf "Cannot create python3 virtual environment in ${dependencies_folder_path}\n" && exit 255; fi

  local -r pip_program_path="${dependencies_folder_path}/bin/pip3"
  "${pip_program_path}" install -U pip setuptools
  if [[ "0" != "$?" ]]; then printf "Cannot execute pip program at ${pip_program_path}\n" && exit 255; fi

  "${pip_program_path}" install poetry
  if [[ "0" != "$?" ]]; then printf "Cannot install poetry at ${pip_program_path}\n" && exit 255; fi

  local -r poetry_program_path="${dependencies_folder_path}/bin/poetry"
  "${poetry_program_path}" install
  if [[ "0" != "$?" ]]; then printf "Cannot execute poetry at ${poetry_program_path}\n" && exit 255; fi

  "${poetry_program_path}" run pytest
  if [[ "0" != "$?" ]]; then printf "Cannot run pytest using poetry program at ${poetry_program_path}\n" && exit 255; fi
}

main
