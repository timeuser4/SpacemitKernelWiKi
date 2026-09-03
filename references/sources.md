# Sources and provenance

Access date for the links below: 2026-09-03.

## Primary chip and platform sources

| Source | URL | Facts used | Version/freshness observed |
|---|---|---|---|
| SpacemiT K1 Datasheet | https://www.spacemit.com/community/document/info?lang=en&nodepath=hardware%2Fkey_stone%2Fk1%2Fk1_docs%2Fk1_ds.md | X60 clusters, RVA22/RVV, caches, TCM, memory, peripherals, AI instruction families | V7.1 dated 2026-08-31 |
| SpacemiT K3 Datasheet | https://www.spacemit.com/community/document/info?lang=en&nodepath=hardware%2Fkey_stone%2Fk3%2Fk3_docs%2Fk3_ds.md | X100/A100/RT24, RVA23, VLEN, caches, memory, I/O, PMU/trace, multimedia | V1.8 dated 2026-08-25; page updated 2026-08-27 |
| SpacemiT K3 Pico-ITX Brief | https://www.spacemit.com/community/document/info?lang=en&nodepath=hardware/eco/k3_pico/root_overview.md | Board dimensions, RAM/UFS, networking, M.2, Type-C, OS and expansion | Page updated 2026-06-10 |
| SpacemiT IME specification repository | https://github.com/spacemit-com/riscv-ime-extension-spec | Public specification scope, supported VLEN range and datatypes | Default branch observed; use releases/commits for pinned work |
| SpacemiT GitHub organization | https://github.com/spacemit-com | Project map, upstream-status dashboard, Linux/llama.cpp/docs/images repositories | Organization page observed 2026-09-03 |
| SpacemiT document center | https://www.spacemit.com/community/document | Canonical navigation for chip, board, and software documents | Live documentation portal |
| SpacemiT release archive | https://archive.spacemit.com/ | OS images and release artifacts | Live archive; select exact version |

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
