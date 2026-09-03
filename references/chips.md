# K-Series chips

This page summarizes published hardware facts. It deliberately contains no optimization result or benchmark conclusion.

## K1 (Key Stone K1)

The K1 is an eight-core 64-bit RISC-V SoC built from two four-core X60 clusters.

| Item | Published value |
|---|---|
| CPU | 8 × SpacemiT X60, two four-core clusters |
| ISA profile | RISC-V 64GCVB, RVA22 |
| Vector | RVV 1.0; 256-bit vector listed at cluster level; X60 section describes VLEN 256/128-bit and 2× execution width |
| AI capability | Vendor-rated 2.0 TOPS through custom RISC-V instructions |
| AI-enabled placement | Cluster 0; cluster 1 is listed without AI capability |
| L1 cache | 32 KiB I-cache + 32 KiB D-cache per core |
| L2 cache | 512 KiB per cluster |
| TCM | 512 KiB in cluster 0 for the AI extension |
| Memory | 32-bit LPDDR4/LPDDR4X up to 16 GiB at 2666 Mbps, or LPDDR3 up to 4 GiB at 1866 Mbps |
| PCIe | Gen2: one ×1 port and two ×2 ports |
| GPU | IMG BXE-2-32, OpenCL 3.0 / OpenGL ES 3.2 / Vulkan 1.3 |
| Video | Decode up to 4K60; encode up to 4K30 for listed codecs |
| Operating range | −40 °C to +85 °C (industrial rating in datasheet) |

### K1 implications for developers

- Do not assume that pinning to any of the eight cores exposes the same custom AI instructions. Determine the Linux CPU numbering for cluster 0 on the actual image and verify it experimentally.
- The official datasheet lists `smt.vmadot*`, `smt.vmadot1*`, `smt.vmadot2*`, and `smt.vmadot3*` custom instruction families and points to the public IME specification.
- Board RAM, storage, wireless, and connector choices vary independently from the SoC capabilities.

## K3

The K3 uses a heterogeneous role split inside a vendor-described homogeneous RISC-V programming model: eight X100 application cores, eight A100 AI cores, and two RT24 real-time cores.

| Item | Published value |
|---|---|
| Application CPU | 8 × X100, 64-bit, four-issue out-of-order, up to 2.4 GHz |
| AI CPU | 8 × A100 with SpacemiT IME |
| Real-time CPU | 2 × RT24, six-stage in-order RV64GC |
| ISA profile | X100: RVA23; A100: vendor-noted RVA23* without Hypervisor extension |
| X100 vector | RVV 1.0, VLEN=256 |
| A100 vector | RVV 1.0, VLEN=1024 |
| Peak AI rating | 60 TOPS at INT4 sparse, as specified for A100 subsystem |
| X100 cache | 64 KiB I + 64 KiB D per core; 4 MiB L2 per cluster; 8 MiB shared across eight cores in overview |
| A100 cache/local memory | 32 KiB I + 32 KiB D per core; 1 MiB L2 and 1.5 MiB scratchpad per cluster |
| Memory | 64-bit LPDDR5-6400 or LPDDR4X-4266, up to 32 GiB; peak 51 GB/s |
| PCIe | 8 × PCIe Gen3 lanes, root-complex and endpoint modes |
| GPU APIs | OpenCL 3.0, OpenGL ES 3.2, Vulkan 1.3 |
| Video | H.264/H.265 up to 4K180 decode and 4K90 encode in current datasheet |
| TDP | 15–25 W |
| Operating range | −40 °C to +85 °C (industrial rating in datasheet) |

### K3 implications for developers

- X100 and A100 are not interchangeable microarchitectures. Code generation, affinity, VLEN assumptions, cache/scratchpad usage, and performance counters must be tied to the executing core type.
- A100 follows a standard CPU programming model but has a substantially wider vector length and IME support. That does not imply that arbitrary X100 binaries automatically exploit A100.
- The K3 datasheet documents RISC-V PMUs on both X100 and A100, plus RISC-V N-Trace-compatible trace blocks. Tool availability still depends on board wiring, firmware, kernel, and image support.

## K1 versus K3

| Dimension | K1 | K3 |
|---|---|---|
| Main generation | X60 | X100 + A100 |
| Profile | RVA22 | RVA23 / RVA23* |
| AI placement | Four-core cluster 0 | Eight dedicated A100 AI cores |
| Published peak AI | 2.0 TOPS | 60 TOPS INT4 sparse |
| Maximum published RAM | 16 GiB LPDDR4/4X | 32 GiB LPDDR5/4X |
| Vector width relevant to AI work | X60 up to 256-bit as documented | A100 VLEN=1024; X100 VLEN=256 |
| Expansion generation | PCIe Gen2 | PCIe Gen3 |

The table is a capability map, not a performance prediction. Compiler support, memory behavior, kernel shape, datatype, sparsity, thermal limits, and software maturity dominate real workloads.
