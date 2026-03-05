# Dreame Mower A1 Pro

[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=flat-square)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/v/release/nicolasglg/dreame-mower-a1-pro?style=flat-square)](https://github.com/nicolasglg/dreame-mower-a1-pro/releases)

**Control your Dreame A1 Pro robotic lawn mower directly from Home Assistant.**

Start, stop, and dock your mower, monitor battery and charging status, and more — all from your HA dashboard.

## What you get

| Entity | Type | What it does |
|--------|------|--------------|
| A1 Pro | Lawn Mower | Start, stop, return to dock |
| Map | Camera | Mowing zone map with named zones and no-go areas |
| Battery Level | Sensor | Current battery percentage |
| State | Sensor | What the mower is doing (mowing, charging, idle, error) |
| Charging Status | Sensor | Charging or not |
| Firmware Version | Sensor | Installed firmware |
| Cleaning Count | Sensor | Total number of mowing sessions |
| Total Cleaning Time | Sensor | Cumulative mowing time (minutes) |
| Total Cleaned Area | Sensor | Cumulative mowed area (m²) |
| First Cleaning Date | Sensor | Date of the very first mow |
| Do Not Disturb | Switch | Enable/disable DnD mode |
| Stop Mowing | Button | Stop current mowing task and return to dock |

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the 3 dots menu > **Custom repositories**
3. Add `nicolasglg/dreame-mower-a1-pro` as **Integration**
4. Search for and install **Dreame Mower A1 Pro**
5. Restart Home Assistant
6. Go to **Settings** > **Integrations** > **Add Integration** > **Dreame Mower**
7. Want to make my day? Buy me a beer or a coffee :) [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/nicolasglg)

### Manual

Copy the `custom_components/dreame_mower` folder to your Home Assistant `custom_components/` directory and restart.

## Configuration

Use the same Dreame / Xiaomi account credentials as the Dreamehome app.

## Compatibility

Tested and working on the **Dreame A1 Pro**. It may work on other Dreame robotic mowers — if you try it on a different model, please [open an issue](https://github.com/nicolasglg/dreame-mower-a1-pro/issues) to let me know how it goes!

## Credits

This integration is a fork of [dreame-mower](https://github.com/bhuebschen/dreame-mower) by [@bhuebschen](https://github.com/bhuebschen), itself based on [dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) by [@Tasshack](https://github.com/Tasshack). It has been reworked to fix cloud connectivity issues, error code mapping, and entity availability specific to the Dreame A1 Pro outdoor mower.
