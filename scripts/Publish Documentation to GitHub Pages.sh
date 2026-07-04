#!/bin/bash

function main() {
  command -v "uv"
  if [[ "0" != "$?" ]]; then printf "Cannot identify uv program\n" && exit 255; fi

  uv run -- mkdocs gh-deploy --clean --force
  local exit_code="$?"
  if [[ "0" != "${exit_code}" ]]; then printf "Cannot run mkdocs using uv program\n" && exit 255; fi
}

main "$@"
