# Changelog

## Unreleased
- Allow definition of queues by django app.
- Allow definition of specific queues file path.

## 1.0.1 - 2022-01-14
### Added
- Close db connections before task body. https://github.com/coleifer/huey/commit/e77acf307bfdade914ab7f91c65dbbc183af5d8f

## 1.0.0 - 2021-05-19
**Note:** This release contains breaking changes, see them below with the migration instructions.

### Added
- Allow definition of a default queue.

### Changed
- HUEYS django setting renamed to DJANGO_HUEY.
- Change command run_djangohuey to djangohuey.

---

## 0.2.0 - 2021-04-18

### Added
*Nothing added this release*

### Changed
*Nothing changed this release*

### Fixed
- When a huey name was not provided, default django db name was used. Now it's defaulted to queue name.

### Removed
- Removed incompatibility with HUEY setting used by [huey](https://github.com/coleifer/huey) project.
