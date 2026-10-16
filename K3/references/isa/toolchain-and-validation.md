# K3 ISA toolchain and validation

This page describes how to establish whether an installed toolchain and runtime can use the K3 instruction set. Hardware documentation and upstream-status pages are not proof that a particular board image contains the same support.

## Upstream status reported by SpacemiT

The SpacemiT K3 toolchain status page reports:

| Toolchain component | X100 | A100 |
|---|---|---|
| LLVM processor definition | Merged | Merged |
| LLVM schedule model | Merged | N/A, listed as same as X60 |
| LLVM vendor extension | N/A, listed as same as X60 | Merged; listed as `xsmtvdotii` |
| LLVM fusion | Merged | N/A, listed as same as X60 |
| GCC processor definition and schedule model | Merged | Merged |
| GCC vendor extension | Not separately listed | Merged |
| Binutils vendor extension | Not separately listed | Merged |

LLVM's own RISC-V usage document lists `XSMTVDotII` as the hardware-adapted A100 IME subset and uses the `smt.` mnemonic prefix. The upstream status is useful for locating support, but the exact installed release and accepted option spellings must be checked locally.

## Record the target environment

Capture the following before interpreting an ISA result:

```bash
cat /proc/device-tree/model 2>/dev/null | tr -d '\0'; echo
cat /proc/cpuinfo
lscpu
uname -a
cat /etc/os-release
getconf GNU_LIBC_VERSION 2>/dev/null || true
gcc --version
clang --version
as --version
ld --version
objdump --version
```

Record the board, SoC revision, OS image, kernel version, firmware, compiler build, target flags, sysroot, libc, assembler, linker, and ABI.

## Compiler and assembler checks

Do not infer an accepted `-march` or `-mcpu` string from a document's subextension name. Check the installed compiler's help, target feature dump, and assembler diagnostics. Vendor extension support may be exposed through a processor name, a vendor feature, inline assembly, builtins, or a target-specific compiler fork.

A standard RVV compiler is not automatically an A100 IME compiler. Conversely, an assembler that accepts a mnemonic does not establish that the resulting binary will execute on the current CPU or that the OS will schedule the thread on an A100.

## Object and opcode checks

After linking:

```bash
readelf -A ./your-binary
objdump -d ./your-binary | less
```

Check that:

- the ELF attributes and target flags match the intended core;
- the expected `smt.*` instructions are present when custom instructions are required;
- no unsupported or unintended code path replaced the custom instruction;
- the surrounding `vset`/vector-state operations satisfy the IME profile;
- the destination and source registers satisfy the relevant overlap and even-register rules.

When the installed disassembler does not recognize an instruction, preserve the raw encoding and compare it with the formal encoding table in the versioned IME source. Do not infer semantics from a mnemonic alone.

## Runtime checks

The executing core must be established independently of the build flags. On K3 Linux images that provide the vendor AI-thread interface, the current bring-up procedure is:

1. In the thread that will execute the test, open `/proc/set_ai_thread`.
2. Write exactly one ASCII `0` and close the file.
3. Apply the intended thread affinity with `pthread_setaffinity_np`.
4. Verify the singleton affinity mask and `sched_getcpu()` in that same thread.
5. Read or verify the vector state required by the test, including VLEN and rounding mode where relevant.
6. Execute the smallest correctness test before integrating a larger operator.

This interface is a Linux image/kernel mechanism, not a portable RISC-V ISA requirement. If the file is absent, do not silently assume that `taskset` or an inherited affinity mask performs the same registration; inspect the image's kernel and vendor runtime implementation.

## Validation matrix

| Check | Why it matters |
|---|---|
| Core identity | X100, A100, and RT24 have different ISA scopes |
| `VLEN` and `LMUL` | A100 IME uses fixed implementation parameters and currently requires `LMUL=1` |
| Signedness and datatype | The mnemonic suffix and encoded datatype select different arithmetic paths |
| Register constraints | Some paths require even `vd`, and sliding/sparse paths require even `vs1` |
| `MCPM.BF16` | Selects FP16 or BF16 behavior in floating and scaled paths |
| Int4 packing | Nibble order affects the interpreted operand values |
| Disassembly | Source-level inline assembly is not proof of final code generation |
| Scalar/reference comparison | Confirms semantics before any performance interpretation |

## What validation does not establish

A successful instruction-level test does not establish instruction latency, issue rate, sustained throughput, model throughput, or the benefit of a kernel optimization. Those require measurements on the exact board, image, compiler, frequency state, data shape, and workload.

## Sources

- [SpacemiT upstream toolchain status](https://github.com/spacemit-com/.github/blob/main/upstream-status/toolchain.md)
- [LLVM RISC-V usage and vendor extensions](https://github.com/llvm/llvm-project/blob/main/llvm/docs/RISCVUsage.md)
- [SpacemiT AI Matrix Extension instruction set](https://github.com/spacemit-com/docs-ai/blob/main/en/architecture/ime_extension.md)
- [K3 datasheet](https://github.com/spacemit-com/docs-chip/blob/main/en/key_stone/k3/k3_docs/k3_ds.md)
