# RT24 ISA and real-time core

## Published hardware profile

The K3 contains two RT24 real-time cores. The K3 datasheet describes RT24 as a 64-bit CVA6-based RISC-V core with a six-stage, in-order, single-issue pipeline.

The published instruction profile is:

- `RV64IMAFDC`, commonly written `RV64GC`.
- RISC-V M, S, and U privilege levels.
- Instruction and data TLBs plus a page-table-walk unit for virtual address translation.

## Applicability

RT24 is described as the K3 system-management core. The public K3 ISA sources do not list RVV, A100 IME, or the A100 `smt.*` instruction families for RT24. Do not use A100 or X100 vector assumptions when targeting RT24.

RT24 instruction availability in a particular image still depends on the firmware, operating system, ABI, and compiler selected for the board.

## Source

- [K3 datasheet, RT24 section](https://github.com/spacemit-com/docs-chip/blob/main/en/key_stone/k3/k3_docs/k3_ds.md#213-rt24-risc-v-core)
