mkdir -p .ctwfs
TMPDIR=.ctwfs

rye run compile-to-wasm-from-scratch $1 > $TMPDIR/compiled.wat

# Run the WAT file
wasm $TMPDIR/compiled.wat -e '(invoke "main")'
