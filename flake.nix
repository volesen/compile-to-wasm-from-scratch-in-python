{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        wasm = pkgs.stdenv.mkDerivation {
          name = "wasm";
          src = pkgs.fetchFromGitHub {
            owner = "WebAssembly";
            repo = "gc";
            rev = "e8529784a15b8b8c11b7e4288d5e55b0b6694bad";
            sha256 = "seWsVjrbqLF0f82k+y8BNaVfYp45Tb6tA77HuN79vBA=";
          };
          buildInputs = with pkgs.ocamlPackages; [ ocaml dune_2 menhir ];
          buildPhase = ''
            cd interpreter
            make
          '';
          installPhase = ''
            mkdir -p $out/bin
            cp wasm $out/bin
          '';
        };
      in
      {
        packages.wasm = wasm;

        devShells.default = pkgs.mkShell {
          buildInputs = [ pkgs.rye wasm ];
        };
      }
    );
}
