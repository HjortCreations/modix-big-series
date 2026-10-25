# Third-party material and earlier permissions

The own-printer license covers Hjort Creations' original contributions only.
It is not a blanket license for every line or fact in this repository.

## Modix configuration and homing references

The homing templates under `firmware/hardware/duet2-duex5/` were adapted from
Modix configuration/macro baselines. They contain Modix-derived structure and
commands alongside Hjort Creations changes. The same exclusion follows those
portions into generated example `sys/home*.g` files.

The public upstream reference is
[Modix V3 configuration and macro files](https://github.com/Modix3D/Modix-V3-configuration-and-Macro-files).
On 25 October 2026 its default-branch tree at commit
`004d389f0e91b22e6413afb8f77ea58ca39f472b` contained no LICENSE, LICENCE or COPYING
file, and GitHub reported no declared license. The reviewed official V4 and
V3-to-V4 BIG-Meter configuration ZIPs also contained no license notice.

**Upstream redistribution permission remains unresolved.** Public availability
does not itself establish permission to relicense or redistribute Modix's
copyrightable material. Hjort Creations does not grant or restrict rights in those
portions. Confirm the applicable permissions with Modix before redistributing
these third-party-derived examples. This notice records the outstanding issue;
it does not resolve it or represent Modix's approval.

Machine dimensions, motor specifications and G-code command names do not become
exclusive Hjort Creations property through the repository license. Follow the
source links in the component documentation for those factual references.

## RepRapFirmware and PrusaSlicer

RepRapFirmware and PrusaSlicer are separate projects and are not bundled here.
Their upstream copyright and licenses remain unchanged:

- [RepRapFirmware](https://github.com/Duet3D/RepRapFirmware), GPL-3.0.
- [PrusaSlicer](https://github.com/prusa3d/PrusaSlicer), AGPL-3.0.

Compatibility with an interpreter does not, on its own, license a script under
the interpreter's license. This is not permission to relicense copied upstream
code; separately licensed upstream material retains its original terms.
See the [GNU interpreter FAQ](https://www.gnu.org/licenses/gpl-faq.en.html#IfInterpreterIsGPL).

## Older Printables profile

The older [BIG-Meter Printables upload](https://www.printables.com/model/889181-print-profile-for-modix-big-meter)
was published under CC0. Rights already granted for that material remain in force,
including where such material is retained in later work. The new license does
not retroactively restrict that material or public-domain contributions.

Do not infer that the older upload's CC0 dedication covers later independent
contributions or material belonging to Modix or other third parties.
