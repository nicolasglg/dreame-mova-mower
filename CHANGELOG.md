# Changelog

## 1.8.9

- Fix A1 Pro zone mowing by using the native mower task API instead of the
  vacuum-derived `START_CUSTOM` segment payload.

## 1.8.8

- Limit maintained hardware support to the Dreame A1 Pro
  (`dreame.mower.g2422`).
- Keep map camera timestamps out of the entity state to reduce Activity and
  recorder noise. The live map and diagnostic update attributes remain
  available.
- Add current mowing zone ID and state sensors for the A1 Pro.
- Add a dynamic charging-aware battery icon.
- Replace vacuum-oriented cleaning labels with mower terminology in English
  and French.
- Fix the recent-change polling condition so the faster interval is only used
  during the intended 60-second window.
- Add A1 Pro-specific issue forms and contribution guidance.

This release intentionally contains no A2, A3, or MOVA-specific changes.
