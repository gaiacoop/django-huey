# Changelog

## 1.1.2 - 2023-11-01
### Fixed
- [#17](https://github.com/gaiacoop/django-huey/issues/17) - Support for python 3.12 and Django 5.0

## 1.1.1 - 2022-02-07
### Fixed
- [#8](https://github.com/gaiacoop/django-huey/issues/8) - Redis was required when using SqliteHuey

## 1.1.0 - 2022-01-18
### Added
- Allow definition of specific queues file path.
- Configuration error is raised if two queues have the same name.

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
