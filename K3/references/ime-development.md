# K3 ISA and IME development index

The detailed K3 instruction-set material is organized under [references/isa/](isa/):

- [K3 instruction-set overview](isa/overview.md): core-to-ISA applicability, standard extensions, vendor subextensions, and evidence rules.
- [X100 ISA and RVV](isa/x100-rvv.md): RVA23, RVV 1.0, VLEN=256, and X100 toolchain status.
- [A100 SpacemiT IME](isa/a100-ime.md): A100 subextensions, instruction families, tile semantics, register constraints, data layout, and encoding summary.
- [RT24 ISA](isa/rt24-rv64gc.md): RV64GC and real-time-core boundary.
- [Toolchain and validation](isa/toolchain-and-validation.md): compiler, assembler, disassembly, runtime-core checks, and correctness validation.

These pages document published ISA behavior and target-validation requirements. They do not contain a particular kernel's tiling, packing, scheduling, benchmark, or optimization result.

## General bring-up sequence

1. Identify the board, SoC revision, OS image, compiler, and executing core.
2. Select the matching versioned chip and ISA documents.
3. Build the smallest instruction-level correctness test.
4. Disassemble the linked binary and confirm the intended instructions.
5. Compare against an independent scalar/reference implementation.
6. Only then collect measurements, keeping raw commands and outputs with the exact target description.
