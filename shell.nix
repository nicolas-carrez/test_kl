{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "django-env";

  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.virtualenv
    pkgs.python312Packages.django
    pkgs.docker
    pkgs.docker-compose
  ];

  shellHook = ''
    if [ ! -d ".venv" ]; then
      python3.12 -m venv .venv
      source .venv/bin/activate
      pip install -r requirements.txt
    else
      source .venv/bin/activate
    fi
  '';
}
