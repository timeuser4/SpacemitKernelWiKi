# K3 instruction-set overview

This page is the entry point for K3 instruction-set information. The K3 is a heterogeneous SoC: instruction availability must be tied to the executing core. A binary or `-march` setting that is valid for X100 does not automatically describe A100, and RT24 is a separate RV64GC real-time core.

## Core-to-ISA map

| Core | Published ISA/profile | Vector and matrix scope | Hypervisor | Applicability |
|---|---|---|---|---|
| X100 application core | RVA23 | RVV 1.0, VLEN=256 | RVH 1.0, GEILEN=8 | General-purpose application code; see [x100-rvv.md](x100-rvv.md) |
| A100 AI core | RVA23* | RVV 1.0, VLEN=1024; SpacemiT IME | Not included in RVA23* | General CPU code plus A100 IME; see [a100-ime.md](a100-ime.md) |
| RT24 real-time core | RV64IMAFDC (`RV64GC`) | No K3 IME support is published | Not listed | System-management and real-time control code; see [rt24-rv64gc.md](rt24-rv64gc.md) |

`RVA23*` is the vendor's A100 profile name. The K3 datasheet explicitly notes that the A100 profile does not include the Hypervisor extension.

## Standard extensions disclosed for X100 and A100

The K3 datasheet lists the following optional extensions for both X100's RVA23 profile and A100's RVA23* profile:

- Vector cryptography: `zvkng`, `zvksg`.
- Other vector and bit-manipulation extensions: `zvbc`, `zfh`, `zbc`, `zvfh`, `zfbmin`, `zvfbfmin`, `zvfbfwma`.
- System and security extensions: `sdtri`, `svvptc`, `sspm`, `smepmp`, `smstateen`, `smcntrpmf`.

The datasheet presents these as optional extensions. Do not assume that every installed compiler, firmware image, kernel, or board configuration exposes every optional extension to user code. Confirm the actual toolchain and target image.

## K3-specific vendor ISA

The K3-specific AI instruction set is the SpacemiT AI Matrix Extension. The public `Zvvm_spacemit` document defines the A100-supported subextensions:

- `Xsmti4i32mm`
- `Xsmti8i32mm`
- `Xsmti8i32mm_slide`
- `Xsmti4i32mm_42sp`
- `Xsmti8i32mm_42sp`
- `Xsmti4fp16mm_scl16f`
- `Xsmti4bf16mm_scl16f`
- `Xsmti8fp16mm_scl16f`
- `Xsmti8bf16mm_scl16f`
- `Xsmtfp16fp32mm`
- `Xsmtbf16fp32mm`
- `Xsmtfp16fp32mm_slide`
- `Xsmtbf16fp32mm_slide`

The same document groups the A100 instructions into seven classes: integer matrix multiplication, floating-point matrix multiplication, integer sliding-window matrix multiplication, floating-point sliding-window matrix multiplication, block-scaled integer matrix multiplication, 4:2 structured-sparse integer matrix multiplication, and data-layout transformation.

The detailed mnemonic list and semantics are in [a100-ime.md](a100-ime.md). These are instruction definitions and implementation parameters, not kernel performance results.

## Other instruction-related facilities

The K3 datasheet also documents facilities that affect instruction bring-up and observability:

- X100 and A100 have RISC-V PMUs.
- X100 and A100 implement RISC-V N-Trace-compatible trace components with branch-trace compression support.
- X100 and A100 support SV39 virtual memory and AIA-related interrupt controllers.
- X100 has RVH 1.0; A100's published RVA23* profile excludes Hypervisor.
- RT24 implements the M, S, and U privilege levels.

Availability of PMU events, trace routing, debug access, and privileged features depends on firmware, kernel, board wiring, and the installed image.

## Reading and evidence rules

1. Establish the executing core before interpreting an ISA string or disassembly.
2. Use the K3 datasheet for core profiles and standard extensions.
3. Use the versioned SpacemiT AI Matrix Extension document for A100 instruction semantics and encodings.
4. Treat compiler, assembler, linker, and debugger support as separate from hardware support.
5. Keep kernel-specific tiling, packing, scheduling, benchmark, and throughput results outside these ISA reference pages.

## Primary sources

- [K3 datasheet](https://github.com/spacemit-com/docs-chip/blob/main/en/key_stone/k3/k3_docs/k3_ds.md)
- [SpacemiT AI Matrix Extension instruction set](https://github.com/spacemit-com/docs-ai/blob/main/en/architecture/ime_extension.md)
- [RISC-V IME extension specification repository](https://github.com/spacemit-com/riscv-ime-extension-spec)
- [SpacemiT upstream toolchain status](https://github.com/spacemit-com/.github/blob/main/upstream-status/toolchain.md)
