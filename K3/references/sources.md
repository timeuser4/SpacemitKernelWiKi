# Sources and provenance

Baseline access date for the original source inventory: 2026-09-03. The latest K3 ISA refresh below was checked on 2026-10-16.

## Primary chip and platform sources

| Source | URL | Facts used | Version/freshness observed |
|---|---|---|---|
| SpacemiT K1 Datasheet | https://www.spacemit.com/community/document/info?lang=en&nodepath=hardware%2Fkey_stone%2Fk1%2Fk1_docs%2Fk1_ds.md | X60 clusters, RVA22/RVV, caches, TCM, memory, peripherals, AI instruction families | V7.1 dated 2026-08-31 |
| SpacemiT K3 Datasheet | https://www.spacemit.com/community/document/info?lang=en&nodepath=hardware%2Fkey_stone%2Fk3%2Fk3_docs%2Fk3_ds.md | X100/A100/RT24, RVA23, VLEN, caches, memory, I/O, PMU/trace, multimedia | V1.9 dated 2026-09-24; direct source checked 2026-10-16 |
| SpacemiT K3 Pico-ITX Brief | https://www.spacemit.com/community/document/info?lang=en&nodepath=hardware/eco/k3_pico/root_overview.md | Board dimensions, RAM/UFS, networking, M.2, Type-C, OS and expansion | Page updated 2026-06-10 |
| SpacemiT IME specification repository | https://github.com/spacemit-com/riscv-ime-extension-spec | Public specification scope, supported VLEN range and datatypes | Default branch observed; use releases/commits for pinned work |
| SpacemiT GitHub organization | https://github.com/spacemit-com | Project map, upstream-status dashboard, Linux/llama.cpp/docs/images repositories | Organization page observed 2026-09-03 |
| SpacemiT document center | https://www.spacemit.com/community/document | Canonical navigation for chip, board, and software documents | Live documentation portal |
| SpacemiT release archive | https://archive.spacemit.com/ | OS images and release artifacts | Live archive; select exact version |

## K3 peak source refresh (2026-10-11)

- [Official direct K3 datasheet](https://cdn-resource.spacemit.com/hardware/docs-chip/en/key_stone/k3/k3_docs/k3_ds.md): V1.9 dated 2026-09-24; SHA256 `ea4cd9af632595fadd60d0bb2835c6ceeacd88e350d0b555919e89f0b6f48996`. Section 2.1.2 confirms 60 TOPS INT4 sparse; no compatible dense i8/i4+FP16 or dense i8 peak is specified.
- [Official CPU manual](https://cdn-resource.spacemit.com/hardware/docs-chip/en/key_stone/k3/k3_docs/k3_usermanual/08_cpu.md): portal update 2026-09-28; SHA256 `38555b1018856094db66fcf4e39dc63fc8b4fdf62e9c71119cf5132817acf9bb`. Section 8.2.2 repeats the sparse INT4 condition.
- The portal UI is an SPA. Use its public [document tree](https://www.spacemit.com/api-server/document/get-doc-tree?language=en) `storgeAddress` field to resolve the document content; HTTP 200 from the UI URL alone does not verify datasheet content.
- Public IME specification pinned at `23b83d93c95f782689d99e8df08fbb6266e875e3` (master). It provides instruction semantics, not A100 throughput/latency. These facts establish the denominator limitation, not a benchmark result.

## A100 instruction source refresh (2026-10-11)

- [SpacemiT AI Matrix Extension instruction set, A100-specific profile](https://github.com/spacemit-com/docs-ai/blob/2b3894e983a295ed0278bc625867e0c132e0e259/en/architecture/ime_extension.md): `Zvvm_spacemit`, version 0.6, Public Release, document updated 2026-04-13. Repository commit `2b3894e983a295ed0278bc625867e0c132e0e259` is dated 2026-09-11T03:46:50Z.
- [Pinned raw source](https://raw.githubusercontent.com/spacemit-com/docs-ai/2b3894e983a295ed0278bc625867e0c132e0e259/en/architecture/ime_extension.md): fetched 2026-10-11, 106687 bytes, SHA256 `8085a55c4671a0b90fa9b5e621772fb66a9fc4733d364fd116de617b9fa6da8e`.
- Sections 2.1.2, 2.3, 2.5, 5.1.3 and 5.4.3 define A100 fixed full i8 and i4 tiles, ordinary Int32 versus HP FP16/BF16 accumulators, register constraints, scale interpretation and LMUL=1. Sections 8.1 and 8.4 define the distinct ordinary and HP encodings. This implementation-specific source takes precedence over generic MAC-shape assumptions from the earlier IME specification.
- The source supplies instruction semantics and geometric work counts, not instruction issue rate, dependent latency, or a dense theoretical compute peak. No measured rate or optimization result is incorporated into this Wiki entry.

## K3 ISA source refresh (2026-10-16)

- [K3 datasheet, official direct source](https://cdn-resource.spacemit.com/hardware/docs-chip/en/key_stone/k3/k3_docs/k3_ds.md): the current published revision is V1.9, dated 2026-09-24. It is the source for the X100, A100, and RT24 core profiles, including the published RVV and standard-extension boundaries.
- [A100 SpacemiT AI Matrix Extension, pinned source](https://github.com/spacemit-com/docs-ai/blob/2b3894e983a295ed0278bc625867e0c132e0e259/en/architecture/ime_extension.md): `Zvvm_spacemit`, version 0.6, Public Release, last updated 2026-04-13; repository commit `2b3894e983a295ed0278bc625867e0c132e0e259`. The pinned raw document has SHA256 `8085a55c4671a0b90fa9b5e621772fb66a9fc4733d364fd116de617b9fa6da8e`.
- [Public RISC-V IME extension repository](https://github.com/spacemit-com/riscv-ime-extension-spec): used for the public extension scope and generic programming-model context; A100-specific implementation values follow the versioned A100 document above.
- [SpacemiT toolchain upstream-status page](https://github.com/spacemit-com/.github/blob/main/upstream-status/toolchain.md) and [LLVM RISC-V usage document](https://github.com/llvm/llvm-project/blob/main/llvm/docs/RISCVUsage.md): used to record upstream compiler, assembler, and vendor-extension naming status. These pages do not prove support in a particular installed toolchain.
- This Wiki records instruction semantics and implementation parameters only. Instruction latency, issue rate, sustained throughput, kernel tiling, packing strategy, scheduling, and model benchmark results require separate target-specific evidence.

## Board-vendor sources

| Source | URL | Facts used |
|---|---|---|
| Banana Pi BPI-F3 documentation | https://docs.banana-pi.org/en/BPI-F3/BananaPi_BPI-F3 | Board form factor, memory/storage options, I/O, source and image links; BPI-CM6 mention |
| Milk-V Jupiter product page | https://milkv.io/jupiter | Mini-ITX form factor, K1/M1, RAM, PCIe signaling, storage, networking, power |
| Sipeed K3 product page | https://sipeed.com/k3 | K3 Pico-ITX/CoM260 positioning, form factors, memory, carrier compatibility, linked PDFs |
| K3 CoM260 developer-kit PDF | https://cdn.sipeed.com/public/k3/SpacemiT%20K3-CoM260%20Developer%20Kit.pdf | Module/developer-kit details |
| K3 Pico-ITX user-guide PDF | https://cdn.sipeed.com/public/k3/SpacemiT%20K3%20Pico-ITX.pdf | Board user-guide details |

## Source policy

Use sources in this order:

1. Versioned chip datasheet, chip manual, board schematic, or board user guide.
2. Vendor documentation portal and official source repository.
3. Board-vendor product page.
4. Upstream project documentation or commits.
5. Third-party reviews only for clearly labeled observations, never as a replacement for electrical or ISA specifications.

When two sources disagree, preserve both values with their document versions and prefer the newer primary document for current work. Do not silently merge specifications from different board revisions.

## Maintenance

When updating this Wiki:

- Record the access date and document revision.
- Update a factual statement and its source entry together.
- Remove stale facts rather than preserving them as “experience.”
- Do not add benchmark conclusions, optimization success stories, or unscoped performance advice to this repository.
