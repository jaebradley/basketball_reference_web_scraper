#!/bin/bash

function main() {
  local -r dependencies_folder_path="$1"
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

  # TODO: @jaebradley re-enable integration pytests
  "${poetry_program_path}" run coverage run --source=basketball_reference_web_scraper --module pytest --ignore "./tests/integration"
  local poetry_exit_code="$?"
  # https://docs.pytest.org/en/7.1.x/reference/exit-codes.html#:~:text=Exit%20code%205,No%20tests%20were%20collected&text=If%20you%20would%20like%20to,using%20the%20pytest%2Dcustom_exit_code%20plugin.
  if [[ "5" == "${poetry_exit_code}" ]]; then printf "pytest using poetry program at ${poetry_program_path} did not collect any tests" && exit 0; fi
  if [[ "0" != "${poetry_exit_code}" ]]; then printf "Cannot run pytest using poetry program at ${poetry_program_path}\n" && exit 255; fi

  "${poetry_program_path}" run coverage report --show-missing
  if [[ "0" != "$?" ]]; then printf "Cannot run coverage report program at ${poetry_program_path}\n" && exit 255; fi
}

main "$@"
