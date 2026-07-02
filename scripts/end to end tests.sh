#!/bin/bash

# TODO: @jaebradley move the duplicative script setup into it's own helper script

function main() {
    # From https://docs.astral.sh/uv/getting-started/installation/
    curl -LsSf https://astral.sh/uv/0.11.26/install.sh | sh
    if [[ "0" != "$?" ]]; then printf "uv installation failed\n" && exit 255; fi

    command -v "uv"
    if [[ "0" != "$?" ]]; then printf "Cannot identify uv program\n" && exit 255; fi

    command -v "uvx"
    if [[ "0" != "$?" ]]; then printf "Cannot identify uvx program\n" && exit 255; fi

    if [[ -f ".venv/bin/activate" ]]; then
      source ".venv/bin/activate"
      if [[ "0" != "$?" ]]; then printf "Could not activate existing virtual environment\n" && exit 255; fi
    else
      uv venv
      if [[ "0" != "$?" ]]; then printf "Cannot create a virtual environment\n" && exit 255; fi
    fi


    uv sync  --active
    if [[ "0" != "$?" ]]; then printf "Cannot install dependencies\n" && exit 255; fi

  uv run coverage run --source=basketball_reference_web_scraper --module pytest \
    --ignore="tests/integration/" \
    --ignore="tests/unit/"

  local tests_exit_code="$?"
    # https://docs.pytest.org/en/7.1.x/reference/exit-codes.html#:~:text=Exit%20code%205,No%20tests%20were%20collected&text=If%20you%20would%20like%20to,using%20the%20pytest%2Dcustom_exit_code%20plugin.
    if [[ "5" == "${tests_exit_code}" ]]; then printf "pytest did not collect any tests" && exit 0; fi
    if [[ "0" != "${tests_exit_code}" ]]; then printf "Cannot run pytest using uv\n" && exit 255; fi
}

main "$@"
