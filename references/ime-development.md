# RVV and IME development

This page explains how to find and verify the applicable instruction documentation. It contains no claim that a particular scheduling, buffering, or unrolling strategy is beneficial.

## Public IME specification

SpacemiT publishes `spacemit-com/riscv-ime-extension-spec`. Its README describes a matrix extension that reuses vector registers and related CSRs, supports VLEN values from 128 to 4096 bits, and covers integer and floating-point types including int4/int8/int16 and fp4/fp8/fp16/bf16.

Use the repository release page for a versioned specification. Pin the release or commit in build and design notes; the default branch is not a stable semantic identifier.

## K1 instruction scope

The current K1 datasheet explicitly lists these custom families on X60 cluster 0:

- Integer dot-product matrix multiply-accumulate: `smt.vmadot`, `smt.vmadotu`, `smt.vmadotsu`, `smt.vmadotus`.
- Sliding-window variants: `smt.vmadot1*`, `smt.vmadot2*`, and `smt.vmadot3*` signed/unsigned combinations.

Use the specification for operand encoding, vector state, element interpretation, accumulator behavior, and corner cases. The mnemonic alone is insufficient to infer those semantics.

## K3 instruction scope

The K3 datasheet describes A100 as an AI-first RISC-V AI-CPU using the SpacemiT-IME instruction set, with RVV 1.0 and VLEN=1024. X100 is separately documented with RVV 1.0 and VLEN=256.

Do not transfer K1 assumptions to K3 merely because both use the term IME. Check the K3 chip manual, compiler support, generated opcode, and executing core.

## Safe bring-up sequence

1. Identify board, SoC revision, OS image, compiler, and executing core.
2. Select a versioned IME specification and the matching vendor chip manual.
3. Build the smallest instruction-level correctness case before integrating a full operator.
4. Disassemble and confirm the intended opcodes and surrounding vector-state instructions.
5. Compare against an independent scalar/reference implementation across boundary sizes and signedness combinations.
6. Profile only after correctness is established; preserve raw command lines and outputs.

## What this Wiki does not establish

- It does not establish instruction latency, throughput, forwarding rules, or undocumented synchronization behavior.
- It does not establish that a kernel optimization is successful.
- It does not establish that K1 and K3 use identical instruction encodings or microarchitectural behavior.
- It does not turn a vendor peak-TOPS number into expected GEMM, model, or token throughput.

Those require a versioned specification or chip manual plus measurements on the exact target.
