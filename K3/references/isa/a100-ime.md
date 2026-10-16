# A100 SpacemiT IME

This page records the A100-specific instruction definitions published in the SpacemiT AI Matrix Extension document. It is an ISA reference, not a kernel-optimization guide. The instruction set is tied to the K3 A100 core; it must not be assumed to run on X100 or RT24.

## Scope and source version

The public source is the `Zvvm_spacemit` profile, version 0.6, marked Public Release and last updated 2026-04-13. It describes the SpacemiT matrix extension as a reuse of the 32 RVV vector registers: vector registers are interpreted as two-dimensional matrix tiles, so the extension does not introduce a separate architectural matrix register file.

The source states that the A100 supports these 13 subextensions:

| Subextension | Function |
|---|---|
| `Xsmti4i32mm` | Int4 matrix multiply with Int32 accumulation |
| `Xsmti8i32mm` | Int8 matrix multiply with Int32 accumulation |
| `Xsmti8i32mm_slide` | Int8 sliding-window matrix multiply with Int32 accumulation |
| `Xsmti4i32mm_42sp` | Int4 4:2 structured-sparse matrix multiply with Int32 accumulation |
| `Xsmti8i32mm_42sp` | Int8 4:2 structured-sparse matrix multiply with Int32 accumulation |
| `Xsmti4fp16mm_scl16f` | Int4 matrix multiply with FP16/BF16 scaling and FP16 output |
| `Xsmti4bf16mm_scl16f` | Int4 matrix multiply with FP16/BF16 scaling and BF16 output |
| `Xsmti8fp16mm_scl16f` | Int8 matrix multiply with FP16/BF16 scaling and FP16 output |
| `Xsmti8bf16mm_scl16f` | Int8 matrix multiply with FP16/BF16 scaling and BF16 output |
| `Xsmtfp16fp32mm` | FP16 matrix multiply with FP32 accumulation |
| `Xsmtbf16fp32mm` | BF16 matrix multiply with FP32 accumulation |
| `Xsmtfp16fp32mm_slide` | FP16 sliding-window matrix multiply with FP32 accumulation |
| `Xsmtbf16fp32mm_slide` | BF16 sliding-window matrix multiply with FP32 accumulation |

The quick index counts 8 base integer instructions, 12 sliding-window instructions, 8 structured-sparse instructions, 8 block-scaled integer instructions, 1 base floating-point instruction, 3 floating-point sliding-window instructions, and 6 data-layout instructions: 46 custom instructions in total when signedness and instruction variants are counted as defined by the source.

## A100 implementation parameters

The implementation parameters are fixed for A100 and are not dynamically selected through `vtype`:

| Instruction group | `VLEN` | `lambda` | `MUL_C` | Accumulator `SEW` | Destination |
|---|---:|---:|---:|---:|---|
| Int4/Int8 Int32 matrix, sliding-window, 4:2 sparse, FP16/BF16 matrix to FP32 | 1024 bits | 4 | 2 | 32 bits | `vd` and `vd+1` |
| Int4/Int8 block-scaled integer matrix | 1024 bits | 8 | 1 | 16 bits | `vd` |

The source defines the matrix operation as:

```text
C <- C + A x B^T
```

The usual operand roles are:

- `vd`: initial accumulator and final destination;
- `vs1`: matrix A;
- `vs2`: matrix B in the implementation-defined hardware-friendly layout;
- `v0` or `v1`: sparse-recovery mask or scale-parameter register in the relevant paths;
- `MCPM.BF16`: implementation control selecting FP16 or BF16 behavior in the relevant instructions.

Only `LMUL=1` is supported by the current profile; other `LMUL` encodings are reserved and must raise an illegal-instruction exception when used by IME instructions.

## Register and overlap rules

For matrix instructions with `MUL_C=2`:

- `vd` must be even and `vd` plus `vd+1` form the destination group.
- The destination group must not overlap `vs1` or `vs2`.
- The standard RVV `vm` mask bit is not used as a matrix-multiply mask control.

For instructions with `MUL_C=1`:

- `vd` may be any vector register.
- `vd` must not overlap `vs1` or `vs2`.

Additional rules:

- Sliding-window instructions require an even-numbered `vs1`.
- Structured-sparse paths use `v0` or `v1` and an `imm2` mask-segment selector.
- Block-scaled paths use `v0` or `v1`, an `imm3` scale-group selector, and `MCPM.BF16`.
- Floating-point paths use `MCPM.BF16` to select FP16 or BF16 input interpretation; mixed FP16/BF16 inputs in one instruction are not defined.

## Matrix instruction families

### Base integer matrix multiply: `smt.vmadot*`

The base path accumulates signed or unsigned integer products into Int32. The signedness suffix describes operand A and operand B:

| Suffix | A | B |
|---|---|---|
| none | signed | signed |
| `u` | unsigned | unsigned |
| `us` | unsigned | signed |
| `su` | signed | unsigned |

The four base mnemonics are:

```text
smt.vmadot
smt.vmadotu
smt.vmadotus
smt.vmadotsu
```

The data type is encoded by the instruction operand form (`i4` or `i8`):

| Path | A x B | A100 tile (`M x K x N`) | Accumulator |
|---|---|---|---|
| `i4` | Int4/UInt4 combinations | `8 x 32 x 8` | Int32 |
| `i8` | Int8/UInt8 combinations | `8 x 16 x 8` | Int32 |

Representative assembly forms are:

```text
smt.vmadot  vd, vs1, vs2, i4
smt.vmadot  vd, vs1, vs2, i8
smt.vmadotu vd, vs1, vs2, i4
smt.vmadotsu vd, vs1, vs2, i8
```

The exact signedness and encoding fields must be taken from the versioned specification.

### Integer sliding-window matrix multiply: `smt.vmadot1/2/3*`

This path is Int8-only. It has the same matrix multiply and Int32 accumulation behavior as the base Int8 path, but reads operand A through a fixed sliding-window offset. The three offsets are represented by `smt.vmadot1*`, `smt.vmadot2*`, and `smt.vmadot3*`; each has the four signedness variants:

```text
smt.vmadot1   smt.vmadot1u   smt.vmadot1us   smt.vmadot1su
smt.vmadot2   smt.vmadot2u   smt.vmadot2us   smt.vmadot2su
smt.vmadot3   smt.vmadot3u   smt.vmadot3us   smt.vmadot3su
```

The A100 tile is `8 x 16 x 8`. `vs1` and `vd` are even-numbered registers. The window may span `vs1` and `vs1+1` according to the instruction definition; this is an operand-access rule, not a recommendation for a particular convolution kernel.

### 4:2 structured-sparse integer matrix multiply: `smt.vmadot.sp*`

For each group of four source elements from A, the instruction reconstructs two elements according to a 4-bit mask, then performs the dot product and accumulates into Int32. The six valid mask patterns are:

```text
1001  1010  1100  0101  0110  0011
```

The instruction family is:

```text
smt.vmadot.sp
smt.vmadotu.sp
smt.vmadotus.sp
smt.vmadotsu.sp
```

The A100 tiles are:

- Int4: `8 x 64 x 8`;
- Int8: `8 x 32 x 8`.

The mask comes from `v0` or `v1`; `imm2` selects one mask segment. `vs1` and `vd` are even-numbered registers. Invalid mask values select no elements and are treated as zero according to the published program-visible semantics.

### Block-scaled integer matrix multiply: `smt.vmadot.hp*`

This path performs an integer dot product, applies a floating-point scale, and accumulates into an FP16 or BF16 destination:

```text
C <- (A x B) x S + C
```

The four signedness variants are:

```text
smt.vmadot.hp
smt.vmadotu.hp
smt.vmadotus.hp
smt.vmadotsu.hp
```

The A100 tiles are:

- Int4: `8 x 32 x 8`;
- Int8: `8 x 16 x 8`.

`v0` or `v1` supplies scale parameters. `imm3` selects one of eight 128-bit scale groups:

| `imm3` | Bits |
|---:|---:|
| 0 | `[127:0]` |
| 1 | `[255:128]` |
| 2 | `[383:256]` |
| 3 | `[511:384]` |
| 4 | `[639:512]` |
| 5 | `[767:640]` |
| 6 | `[895:768]` |
| 7 | `[1023:896]` |

`MCPM.BF16` selects whether the 16-bit scale and destination path uses FP16 or BF16. The destination is one vector register because `MUL_C=1`.

### Floating-point matrix multiply: `smt.vfwmadot`

The base floating-point path supports same-format FP16×FP16 or BF16×BF16 input and FP32 accumulation:

```text
smt.vfwmadot vd, vs1, vs2
```

The A100 tile is `8 x 8 x 8`. `MCPM.BF16=0` selects FP16 inputs; `MCPM.BF16=1` selects BF16 inputs. Mixed FP16/BF16 inputs in one instruction are not defined. This path uses the `MUL_C=2`, even-`vd` destination rules.

### Floating-point sliding-window matrix multiply: `smt.vfwmadot1/2/3`

The floating-point sliding-window family is:

```text
smt.vfwmadot1
smt.vfwmadot2
smt.vfwmadot3
```

It uses FP16 or BF16 input selected by `MCPM.BF16`, accumulates into FP32, and requires an even-numbered `vs1` for the windowed access. The precise window semantics and encodings are defined in the source specification.

## Data layout transformation instructions

The six layout instructions are:

```text
smt.vpack.vv
smt.vupack.vv
smt.vnpack.vv
smt.vnspack.vv
smt.vnpack4.vv
smt.vnspack4.vv
```

Their published functions are:

| Instruction | Function |
|---|---|
| `smt.vpack.vv` | Interleave two source streams |
| `smt.vupack.vv` | De-interleave an interleaved stream |
| `smt.vnpack.vv` | Narrow and interleave |
| `smt.vnspack.vv` | Saturating narrow and interleave |
| `smt.vnpack4.vv` | Narrow and pack to 4-bit elements |
| `smt.vnspack4.vv` | Saturating narrow and pack to 4-bit elements |

For `vpack` and `vupack`, `imm2` selects element-width, 128-bit, 256-bit, or 512-bit packing. For the narrowing and 4-bit packing forms, `imm2` selects 32-bit, 64-bit, 128-bit, or 256-bit packing. If the selected packing length exceeds `VLEN x LMUL`, the instruction is illegal.

For packed Int4 data, the profile defines element `2n` in bits `[3:0]` of byte `n` and element `2n+1` in bits `[7:4]` of byte `n`.

## Encoding summary

The custom matrix instructions use the 32-bit custom opcode `0101011` in the published encoding tables. The main encoding fields select:

- data type (`DT`), including Int4 or Int8 where applicable;
- signedness or instruction family;
- source and destination vector registers;
- `imm2` for sparse-mask or layout selection;
- `imm3` for block-scale selection;
- a selector for `v0` or `v1` in sparse and scale paths.

The base integer path requires an even `vd`; the sliding-window and sparse paths additionally encode the even-register restriction on `vs1`. The floating-point sliding-window encodings use the low function field to select slide 1, 2, or 3.

Use the formal encoding tables in the versioned source when assembling raw instructions. This page intentionally summarizes the fields and does not replace the bit-level source of truth.

## Toolchain naming and support

LLVM's current RISC-V usage documentation lists `XSMTVDotII` as the hardware-adapted A100 IME subset and documents `smt.` instruction prefixes. SpacemiT's upstream-status page reports A100 processor definition, GCC processor/schedule model, A100 vendor extension, and Binutils vendor extension work as merged in its K3 status table.

Those status entries do not guarantee support in the compiler installed on a target board, nor do they establish that all 46 instructions are available through C/C++ intrinsics. Confirm assembler acceptance and inspect the final object with a target-appropriate disassembler.

## Correctness and portability boundary

- Identify the actual executing core and SoC revision.
- Confirm the OS image, kernel interface, compiler, assembler, linker, and ABI.
- Build a minimal instruction-level correctness test for each instruction family used.
- Verify register constraints, `LMUL`, `MCPM.BF16`, signedness, data packing, and full output layout.
- Disassemble the linked binary and verify the intended `smt.*` instructions.
- Compare with an independent scalar/reference implementation.
- Keep measured latency, throughput, scheduling, tiling, packing strategies, and model-specific results in separate experiment records.

## Sources

- [SpacemiT AI Matrix Extension instruction set, `Zvvm_spacemit` profile](https://github.com/spacemit-com/docs-ai/blob/2b3894e983a295ed0278bc625867e0c132e0e259/en/architecture/ime_extension.md)
- [Public RISC-V IME extension repository](https://github.com/spacemit-com/riscv-ime-extension-spec)
- [K3 datasheet, A100 section](https://github.com/spacemit-com/docs-chip/blob/main/en/key_stone/k3/k3_docs/k3_ds.md#212-spacemit-a100-ai-core)
- [SpacemiT upstream toolchain status](https://github.com/spacemit-com/.github/blob/main/upstream-status/toolchain.md)
- [LLVM RISC-V usage and vendor-extension status](https://github.com/llvm/llvm-project/blob/main/llvm/docs/RISCVUsage.md)
