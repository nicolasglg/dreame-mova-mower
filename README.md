# Dreame Mower A1 Pro

Home Assistant integration for the **Dreame A1 Pro** robotic lawn mower.

Fork of [dreame-mower](https://github.com/bhuebschen/dreame-mower) by [@bhuebschen](https://github.com/bhuebschen), itself based on [dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) by [@Tasshack](https://github.com/Tasshack).

## Entities

| Entity | Type | Description |
|--------|------|-------------|
| A1 Pro | Lawn Mower | Main entity — start, stop, dock |
| Battery Level | Sensor | Current battery percentage |
| State | Sensor | Current state (mowing, charging, idle, error) |
| Charging Status | Sensor | Charging / not charging |
| Firmware Version | Sensor | Installed firmware version |
| DnD | Switch | Do Not Disturb mode |

## What was fixed from the original

- **Error codes**: Remapped vacuum error codes to mower-specific meanings (e.g. code 48 = "Mowing Complete", not "LDS Error")
- **Cloud timeouts**: Increased HTTP timeouts from 5s to 15s for outdoor devices with intermittent WiFi
- **Connection stability**: MQTT connection kept alive even when cloud HTTP requests fail
- **Startup reliability**: Integration no longer crashes when initial property requests timeout
- **Removed unavailable entities**: Stripped camera, map, and cleaning history entities that require cloud features unavailable on the A1 Pro

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the 3 dots menu > **Custom repositories**
3. Add `nicolasglg/dreame-mower-a1-pro` as **Integration**
4. Search for and install **Dreame Mower A1 Pro**
5. Restart Home Assistant
6. Go to Settings > Integrations > Add Integration > **Dreame Mower**

### Manual

Copy the `custom_components/dreame_mower` folder to your Home Assistant `custom_components/` directory and restart.

## Configuration

Use the same Dreame / Xiaomi account credentials as the Dreamehome app.

## Credits

- [@bhuebschen](https://github.com/bhuebschen) — original [dreame-mower](https://github.com/bhuebschen/dreame-mower) integration
- [@Tasshack](https://github.com/Tasshack) — [dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) integration this is based on

## Support

If this integration is useful to you:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/nicolasglg)
