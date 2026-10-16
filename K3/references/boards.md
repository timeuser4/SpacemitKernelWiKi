# Boards and modules

Use the board vendor's current schematic and user guide for electrical work. The summaries below are selection aids, not substitutes for those documents.

## K1 ecosystem

### Banana Pi BPI-F3

Industrial-oriented K1 SBC in a 148 × 100 mm form factor.

- K1, 8 × X60, RVA22 and RVV 1.0.
- 2/4/8/16 GiB LPDDR4 options.
- Optional 8/16/32/128 GiB eMMC plus microSD.
- Two Gigabit Ethernet ports, four USB 3.0 host ports, USB 2.0 Type-C OTG.
- M.2 M-key via PCIe Gen2 ×2 and mini-PCIe via one lane.
- HDMI 1.4, MIPI DSI, dual-camera support, 26-pin GPIO header.
- Vendor page links Bianbu, OpenWrt, Linux/U-Boot/OpenSBI sources, schematics, images, and flashing tools.

The same vendor page also identifies BPI-CM6 as a K1 compute-module design. Treat its carrier-board interfaces separately from BPI-F3.

### Milk-V Jupiter

Mini-ITX K1/M1 desktop and NAS-oriented board.

- K1/M1, 8 × X60, RVA22 and RVV 1.0.
- 4/8/16 GiB LPDDR4X.
- M.2 NVMe (PCIe 2.0 ×2), eMMC connector, microSD, boot SPI flash.
- Physical PCIe ×8 slot carrying PCIe 2.1 ×2 signaling.
- Two Gigabit Ethernet ports, Wi-Fi 6/Bluetooth 5.2.
- Standard 24-pin ATX input plus 12 V DC input.
- Vendor positions the board for desktop and NAS use and lists optimized Ubuntu/Fedora support.

Do not infer eight electrical PCIe lanes from the mechanical ×8 connector.

## K3 ecosystem

### SpacemiT K3 Pico-ITX

Compact 100 × 86 mm Pico-ITX Plus SBC.

- K3 with 8 X100 cores and 8 A100 AI cores; vendor-rated 60 TOPS.
- 16 or 32 GiB dual-channel LPDDR5-6400.
- 128 or 256 GiB UFS 2.2.
- M.2 M-key PCIe Gen3 ×4 for NVMe; M.2 B-key PCIe/USB expansion.
- Gigabit RJ45 plus 10GbE SFP+.
- Wi-Fi 6/Bluetooth 5.2.
- Two USB 3.2 Gen1 Type-C connectors; one supports 65 W PD and 4K DisplayPort.
- RT24-connected real-time expansion exposes EtherCAT, CAN-FD, SPI, I²C, UART and related signals through an optional board.
- Preinstalled Bianbu 3.0; official page also lists Ubuntu 26.04 and other distributions.

The B-key and M-key slots share lanes: when both are populated, the M-key link operates at PCIe Gen3 ×2 according to the official brief.

### K3 CoM260 and developer kit

The K3 CoM260 is a 69.6 × 45 mm, 260-pin SO-DIMM module promoted with 16/32 GiB LPDDR5 unified-memory options. Sipeed describes the module and development kit as carrier-compatible with the Jetson Orin family.

Compatibility claims must be checked at three levels before reuse:

1. Mechanical connector and mounting.
2. Pin assignment, voltage, lane routing, and power sequencing.
3. Boot firmware, device tree, drivers, and operating-system image.

Use the current CoM260 developer-kit PDF rather than assuming every Orin carrier peripheral is software-compatible.

## Selection guide

| Need | Candidate | Reason to inspect first |
|---|---|---|
| K1 kernel/IME bring-up with exposed I/O | BPI-F3 | Detailed public board page, schematics/resources, broad I/O |
| K1 desktop or NAS | Milk-V Jupiter | Mini-ITX, ATX power, storage and PCIe slot |
| Compact self-contained K3 system | K3 Pico-ITX | Onboard RAM/UFS, 10GbE, dual M.2, Type-C PD |
| K3 carrier integration | K3 CoM260 kit | Compute-module form factor and carrier ecosystem |

Availability, BOM revision, memory population, and OS-image maturity change over time; verify them at purchase and deployment time.
