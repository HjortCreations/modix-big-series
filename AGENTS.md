# Maintenance rules

- Write repository documentation, code comments, user-facing messages and release notes in English.
- This repository contains reusable components. Keep customer names, addresses, IP/MAC addresses, controller UIDs, CRM IDs, passwords, network settings and service notes in private local service records outside the repository.
- Update the appropriate component instead of adding a complete machine copy. Keep model geometry out of toolhead, material and process profiles. Material and process profiles must not depend on model names.
- firmware/common/stop.g, firmware/common/g32_u.g and slicer/gcode/ are the sole sources for their respective shared routines. Never edit generated copies manually.
- Do not version config_probe.g, PID files, M556 values, input-shaper settings, network configuration or individual machine calibration. Preserve each machine's working configuration and local backup.
- Changes to motion limits, temperatures or algorithms must be intentional and separate from cleanup. Never describe a repository cleanup as physical testing.
- A recipe selects model, geometry, hardware, toolhead/nozzle, process, material and motion components. State the actual validation status. A model name does not establish wiring, homing direction or probe offsets.
- Never load optional motor tuning automatically. Document its assumptions and rollback parameters.
- Run python tools/check.py and build every package. For slicer changes, also perform actual PrusaSlicer CLI slicing as described in docs/validation.md. Check start/end commands, temperatures, limits and flow.
- Update the existing short documents in place. Do not add dated service narratives, screenshots, log directories, abandoned test profiles or alternative final/v2 files.
- dist/, local profiles and review logs are ignored. Build release packages from an identified commit. Keep secrets out of Git history.
- Building or testing must not install files on a printer or operate it. Deployment is a separate action governed by the user's instructions and the current machine state.
