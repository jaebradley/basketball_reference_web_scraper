#!/bin/bash

function main() {
  local -r poetry_program_path="$1"
  if [[ ! -e "${poetry_program_path}" ]]; then printf "Cannot execute poetry at ${poetry_program_path}\n" && exit 255; fi

  "${poetry_program_path}" run -- mkdocs gh-deploy --clean --force
  local poetry_exit_code="$?"
  if [[ "0" != "${poetry_exit_code}" ]]; then printf "Cannot run mkdocs using poetry program at ${poetry_program_path}\n" && exit 255; fi
}

main "$@"
