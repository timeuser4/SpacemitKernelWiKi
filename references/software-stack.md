# Software stack and discovery

## Start with the installed system

Before choosing a toolchain or image, capture the actual environment:

```bash
cat /proc/device-tree/model 2>/dev/null | tr -d '\0'; echo
cat /proc/cpuinfo
lscpu
uname -a
cat /etc/os-release
getconf GNU_LIBC_VERSION 2>/dev/null || true
```

For toolchain and binary inspection:

```bash
gcc -v
clang --version
ld --version
objdump --version
readelf -A ./your-binary
objdump -d ./your-binary | less
```

Record the compiler build, target flags, sysroot, libc, and exact OS image. Distribution names alone do not identify ISA defaults.

## Official software entry points

- SpacemiT document center: chip manuals, board guides, software manuals, and hardware resources.
- SpacemiT archive: downloadable images and release artifacts.
- SpacemiT GitHub organization: upstream-status dashboard plus maintained/forked Linux, llama.cpp, IME specification, Bianbu documentation, chip documentation, AI documentation, and K3 Ubuntu image repositories.
- Bianbu sources referenced by board vendors: Linux, U-Boot, and OpenSBI repositories are commonly split rather than delivered as one monorepo.

The GitHub organization landing page maintains a dated K1/K3 upstream-status table. Treat each row as a status pointer and follow its detail page or upstream commit before claiming support in a particular release.

## OS families seen in official material

- Bianbu is SpacemiT's primary Debian-derived distribution and image family.
- K1 board vendors publish or link Bianbu, Ubuntu/Armbian, Fedora, Debian, OpenWrt, and other community images depending on board and revision.
- The K3 Pico-ITX brief lists Bianbu 3.0 preinstallation and names Ubuntu 26.04, OpenHarmony 6.0, OpenKylin, Deepin, and Fedora as supported systems.
- SpacemiT publishes a `K3-Ubuntu-Images` repository for building and flashing UEFI-bootable Ubuntu images for K3 Pico-ITX.

“Supported” can mean vendor image, community image, upstream kernel support, or a validated application stack. State which meaning applies.

## Runtime placement

Custom ISA availability may depend on core placement. Capture and control affinity explicitly:

```bash
taskset -pc $$
taskset -c <cpu-list> ./your-binary
```

Inside a test program, print `sched_getcpu()` after binding. On K1, map Linux CPU IDs to the AI-enabled cluster using the board's current device tree or vendor documentation. On K3, map execution to X100 versus A100 rather than relying on total CPU count.

## Build portability rules

- Verify the accepted `-march`/`-mcpu` options in the installed compiler; do not assume a compiler that supports standard RVV also recognizes vendor IME mnemonics.
- Keep a standard-RISC-V or scalar fallback when distributing beyond a fixed image and board.
- Confirm custom opcodes in the linked binary. Inline assembly present in source may be removed, rejected, or routed through a different code path.
- Pair binaries with their required OS image, loader, libc, and firmware versions in experiment notes.
