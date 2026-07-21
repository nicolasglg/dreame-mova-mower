# Dreame Mower A1 Pro

[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=flat-square)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/v/release/nicolasglg/dreame-mower-a1-pro?style=flat-square)](https://github.com/nicolasglg/dreame-mower-a1-pro/releases)

> ⚠️ **Scope of support**
>
> This repository supports the **Dreame A1 Pro** (`dreame.mower.g2422`) only. It is the only mower I own and can test responsibly before every release.
>
> Unfortunately, I cannot maintain other Dreame or MOVA mower models. Existing code may still happen to work with some of them, but model-specific issues and feature requests will be closed as out of scope. Community forks are very welcome.

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
| Current Zone ID | Sensor | ID of the zone currently being mowed |
| Current Zone State | Sensor | Raw A1 Pro state of the active zone |
| Mowing Sessions | Sensor | Total number of mowing sessions |
| Total Mowing Time | Sensor | Cumulative mowing time (minutes) |
| Total Mowed Area | Sensor | Cumulative mowed area (m²) |
| First Mowing Date | Sensor | Date of the very first mow |
| Do Not Disturb | Switch | Enable/disable DnD mode |
| Stop Mowing | Button | Stop current mowing task and return to dock |
| Error notification | Persistent notification | Automatic alert when the mower reports an error (translated in FR/EN) |

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the 3 dots menu > **Custom repositories**
3. Add `nicolasglg/dreame-mower-a1-pro` as **Integration**
4. Search for and install **Dreame Mower A1 Pro**
5. Restart Home Assistant
6. Go to **Settings** > **Integrations** > **Add Integration** > **Dreame Mower**
7. Want to make my day? Buy me a beer :) [![Buy Me A Beer](https://img.shields.io/badge/Buy%20Me%20A%20Beer-support-yellow?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/nicolasglg)

### Manual

Copy the `custom_components/dreame_mower` folder to your Home Assistant `custom_components/` directory and restart.

## Configuration

Use the same Dreame / Xiaomi account credentials as the Dreamehome app.

### Reduce map activity and history

Map cameras update whenever the mower publishes a new map frame. If you do not
need their history, you can keep the live maps while excluding their state
changes from Home Assistant's Activity panel and recorder database:

```yaml
logbook:
  exclude:
    entity_globs:
      - camera.*_map
      - camera.*_map_*

recorder:
  exclude:
    entity_globs:
      - camera.*_map
      - camera.*_map_*
```

Use the exact entity IDs instead of these globs if another integration also
creates camera entities whose IDs contain `_map`.

## Supported model

| Model | Status | Notes |
|-------|--------|-------|
| Dreame A1 Pro (`dreame.mower.g2422`) | Officially supported | Tested by me on every release |

Please open issues only for the A1 Pro and include the model ID shown by the Dreame app or Home Assistant diagnostics.

## Credits

This integration is a fork of [dreame-mower](https://github.com/bhuebschen/dreame-mower) by [@bhuebschen](https://github.com/bhuebschen), itself based on [dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) by [@Tasshack](https://github.com/Tasshack). It has been reworked to fix cloud connectivity issues, error code mapping, and entity availability specific to the Dreame A1 Pro outdoor mower.
