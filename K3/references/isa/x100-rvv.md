# X100 ISA and RVV

## Published hardware profile

The K3 X100 is an eight-core, 64-bit, four-issue, out-of-order RISC-V application core. The K3 datasheet identifies it as RVA23-compliant and lists RVV 1.0 with `VLEN=256`.

The datasheet also lists `RVH 1.0` with `GEILEN=8`, RISC-V PMU support, SV39 virtual memory, AIA-related interrupt support, RISC-V debug/trace support, and the optional RVA23 extensions listed below.

## Optional extensions listed for X100

- `zvkng`, `zvksg`
- `zvbc`, `zfh`, `zbc`, `zvfh`, `zfbmin`, `zvfbfmin`, `zvfbfwma`
- `sdtri`, `svvptc`, `sspm`, `smepmp`, `smstateen`, `smcntrpmf`

These are the extensions disclosed by the current K3 datasheet. The datasheet does not replace the installed system's ISA discovery or the compiler's accepted extension list.

## Vector programming boundary

X100 uses the standard RISC-V Vector programming model. The public K3 sources do not assign the A100-specific SpacemiT IME subextensions to X100. Do not infer that an X100 thread can execute A100 `smt.vmadot*`, `smt.vfwmadot*`, or layout-transformation instructions merely because both cores implement RVV.

`VLEN=256` is an X100 hardware parameter. It does not mean that an A100 binary can be retargeted by changing only a vector-length assumption; A100 has a separate `VLEN=1024` implementation and a different IME capability set.

## Toolchain status

SpacemiT's upstream-status page reports the following K3 toolchain work:

- LLVM X100 processor definition: merged.
- LLVM X100 schedule model: merged.
- LLVM X100 vendor extension: listed as N/A, described there as the same as X60.
- LLVM X100 fusion: merged.
- GCC X100 processor definition and schedule model: merged in the June 2026 status entry.

A status entry means that upstream work exists; it does not prove that a particular compiler package installed on a board contains that work. Record the compiler version, target options, sysroot, assembler, linker, and disassembly when validating X100 code generation.

## What this page does not claim

This page does not enumerate every standard RVV instruction or claim a particular vectorization, scheduling, cache, or tiling strategy is faster. Those are compiler- and workload-specific questions that require a target build and measurement.

## Sources

- [K3 datasheet, X100 section](https://github.com/spacemit-com/docs-chip/blob/main/en/key_stone/k3/k3_docs/k3_ds.md#211-spacemit-x100-risc-v-core)
- [SpacemiT upstream toolchain status](https://github.com/spacemit-com/.github/blob/main/upstream-status/toolchain.md)
