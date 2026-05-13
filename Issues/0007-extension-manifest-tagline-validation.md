# 0007 Extension Manifest Tagline Validation

- Priority: P3
- Status: done
- Phase: 06-release
- Linked TODO: [TODO.md](../TODO.md)

## Contract

The packaged add-on must pass Blender extension validation. Blender 5.1 rejects `blender_manifest.toml` when `tagline` is longer than 64 characters.

## Checklist

- [x] Shorten `blender_manifest.toml` tagline to 64 characters or fewer.
- [x] Regenerate add-on ZIP.
- [x] Make runtime gate regenerate the add-on ZIP before validation.
- [x] Run `npm run runtime:gate` with the Steam Blender path.
- [x] Update release and QCDS evidence.

## Evidence

`dist/extension-validate.log` reported:

```text
FATAL_ERROR: key "tagline" invalid: a value no longer than 64 characters expected, found 66
```

After shortening the tagline, Blender 5.1.1 extension validation passed.
