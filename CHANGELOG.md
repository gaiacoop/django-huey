# Changelog

## Unreleased
- Allow definition of a default queue.
- Allow definition of queues by django app.
- Allow definition of specific queues file path.

## 1.0.0 - 
**Note:** This release contains breaking changes, see them below with the migration instructions.


### Changed
- HUEYS django setting renamed to DJANGO_HUEY.
- Change command run_djangohuey to djangohuey.


### Breaking Changes
#### *HUEYS django setting renamed to DJANGO_HUEY.*

##### Migration steps: 
In *django settings* change:
```python
HUEYS = {...} #Queues definition
```

to the following:
```python
DJANGO_HUEY = {...} #Queues definition
```

#### *Change command run_djangohuey to djangohuey.*

##### Migration steps: 
Before this release you run the queue consumer with the following command:
```bash
python manage.py run_djangohuey --queue first
```

Now you run:
```bash
python manage.py djangohuey --queue first
```
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
