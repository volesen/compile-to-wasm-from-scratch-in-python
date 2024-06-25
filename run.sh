TMPDIR=$(mktemp -d)

rye run compile-to-wasm-from-scratch $1 > $TMPDIR/compiled.wasm

# Compile the WAT file to a WASM file
wat2wasm $TMPDIR/compiled.wasm -o $TMPDIR/compiled.wasm

# Run the WASM file
wasm-interp $TMPDIR/compiled.wasm --run-all-exports
