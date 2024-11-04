{ ... }:

{
  # https://devenv.sh/languages/
  languages.python.enable = true;
  languages.python.poetry.enable = true;
  languages.python.poetry.activate.enable = true;
  languages.python.poetry.install.enable = true;
  languages.python.directory = ".";

  # https://devenv.sh/pre-commit-hooks/
  # lint shell scripts
  pre-commit.hooks.shellcheck.enable = true;
  # execute example shell from Markdown files
  pre-commit.hooks.mdsh.enable = true;
  # format Python code
  pre-commit.hooks.black.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
