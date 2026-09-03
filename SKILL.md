---
name: spacemit-kernel-wiki
description: Identify and develop for SpacemiT K-series RISC-V chips and boards, especially K1/X60 and K3/X100+A100 platforms. Use when comparing hardware, selecting a board, locating official SDK/OS/ISA material, checking RVV or IME availability, or preparing portable kernel work. This is a sourced platform wiki, not a record of past optimization results.
---

# SpacemiT K-Series Kernel Wiki

Use this skill to establish the exact chip, core type, board, software stack, and authoritative documentation before discussing kernels. Do not treat an optimization attempted on one machine as evidence for another machine—or as a generally successful technique.

## Route the question

- For K1 and K3 architecture, core, cache, memory, vector, and AI-compute facts, read [references/chips.md](references/chips.md).
- For board and module selection, connectors, memory/storage options, and form factors, read [references/boards.md](references/boards.md).
- For Bianbu, Linux, toolchains, upstream repositories, and system discovery, read [references/software-stack.md](references/software-stack.md).
- For RVV/IME kernel development and instruction-document routing, read [references/ime-development.md](references/ime-development.md).
- For provenance, document versions, update dates, and confidence boundaries, read [references/sources.md](references/sources.md).

Use `scripts/query.py <terms>` when the relevant page is unclear.

## Required distinctions

1. Identify the board and SoC separately. A board specification is not automatically a complete chip specification.
2. On K1, distinguish cluster 0 from cluster 1: the official datasheet assigns the AI custom-instruction capability and TCM to cluster 0.
3. On K3, distinguish X100 application cores, A100 AI cores, and RT24 real-time cores. Their vector length, cache hierarchy, virtualization support, and intended workloads differ.
4. Report theoretical TOPS only as a vendor-rated peak with its stated datatype/sparsity condition. Never convert it directly into expected application throughput.
5. Treat K1 and K3 binaries as target-specific until the required ISA extensions, ABI, OS image, and runtime dispatch have been verified.
6. Separate sourced facts from inference. If a fact is not present in an authoritative source, label it unknown instead of filling the gap from a related board or generation.

## Kernel-work checklist

Before building or profiling, collect:

```bash
cat /proc/device-tree/model 2>/dev/null | tr -d '\0'
lscpu
uname -a
cat /etc/os-release
gcc --version
clang --version
taskset -pc $$
```

Then confirm the executing core with `sched_getcpu()` or an equivalent affinity check. For custom instructions, inspect the final object with `objdump -d` and verify execution on the intended core type.

## Output contract

State the detected or assumed chip, core type, board, OS/toolchain, and source URLs. When comparing products, include only like-for-like fields and mark unavailable values as unknown. Do not cite this Wiki as benchmark evidence; cite the original measurement artifact for any performance claim.
