# Worked example: select available inventory

The task is to expose a function that selects available items. This Python example uses `pytest`; substitute the project's language and test runner while preserving the cycle. It illustrates two successive behaviors rather than a complete application.

## First behavior: exclude unavailable items

Write the caller before the implementation in `tests/test_inventory.py`:

```python
from inventory import available_items


def test_excludes_unavailable_items():
    items = [
        {"id": "a", "available": True},
        {"id": "b", "available": False},
    ]
    assert available_items(items) == [items[0]]
```

Run `pytest tests/test_inventory.py`. A missing `inventory` module or missing exported function is the intended initial failure only after confirming that the project's import path and runner configuration are valid. If a declaration is needed to make collection work, add a minimal stub and observe the behavioral assertion fail before implementing filtering.

Implement only that behavior in `inventory.py`:

```python
def available_items(items):
    return [item for item in items if item["available"]]
```

Rerun the test and confirm green. Review readability and duplication; if no refactor is useful, proceed. Do not add reservation or stock rules yet.

## Next behavior: exclude reserved items

Add one test:

```python
def test_excludes_reserved_items():
    items = [
        {"id": "a", "available": True, "reserved": False},
        {"id": "b", "available": True, "reserved": True},
    ]
    assert available_items(items) == [items[0]]
```

Run it: the existing implementation includes both items, so the assertion fails. Now implement the smallest change, treating an absent reservation flag as false to preserve the first case:

```python
def available_items(items):
    return [
        item for item in items
        if item["available"] and not item.get("reserved", False)
    ]
```

Run both tests. They should pass. If future cases share the same setup and assertion, convert them to parameterized cases while keeping the suite green. Add new behavior one failing case at a time.

## When a private helper grows

Suppose stock and reservation rules grow into `_eligible(item)`. Its existence does not require a direct private-helper test. Keep driving the selection result through `available_items` if eligibility is only an implementation detail.

If eligibility becomes a cohesive policy used by several real consumers, extract a component with a supported `is_eligible(item)` API. Drive that API with its own failing behavioral test. Independent responsibility and real callers justify extraction; access from a test alone does not.
