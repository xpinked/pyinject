from typing import Any, Literal

import pytest

from pyinject.manager import DependenciesManager, OverridesMapping, _Dependency


def mock_dependency_callable() -> Literal["dependency_value"]:
    return "dependency_value"


def mock_override_callable() -> Literal["override_value"]:
    return "override_value"


@pytest.mark.parametrize(
    "test_id, dependency, expected",
    [
        ("happy-path-no-cache", _Dependency(mock_dependency_callable, cache=False), "dependency_value"),
        ("happy-path-with-cache", _Dependency(callable=mock_dependency_callable, cache=True), "dependency_value"),
        ("happy-path-override", _Dependency(mock_dependency_callable, cache=False), "override_value"),
    ],
    ids=lambda test_id: test_id,
)
def test_get_dependency_value_happy_path(
    test_id: Literal["happy-path-no-cache", "happy-path-with-cache", "happy-path-override"],
    dependency: _Dependency,
    expected: Literal["dependency_value", "override_value"],
):
    manager = DependenciesManager()

    old_overrides: OverridesMapping | None = None

    if test_id == "happy-path-override":
        old_overrides = manager.override_dependencies({mock_dependency_callable: mock_override_callable})

    result = manager.get_dependency_value(dependency)

    if test_id == "happy-path-override" and old_overrides is not None:
        manager.restore_dependencies({mock_dependency_callable: mock_override_callable}, old_overrides)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "test_id, dependency, overrides, expected",
    [
        (
            "edge-case-override-cache",
            _Dependency(callable=mock_dependency_callable, cache=True),
            {mock_dependency_callable: mock_override_callable},
            "override_value",
        ),
    ],
    ids=lambda test_id: test_id,
)
def test_get_dependency_value_edge_cases(
    test_id: Literal["edge-case-override-cache"],
    dependency: _Dependency,
    overrides: OverridesMapping,
    expected: Literal["override_value"],
):
    manager = DependenciesManager()

    manager.override_dependencies(overrides)

    result = manager.get_dependency_value(dependency)

    assert result == expected


@pytest.mark.parametrize(
    "test_id, dependency, exception",
    [
        ("error-null-callable", _Dependency(None, cache=False), ValueError),
    ],
    ids=lambda test_id: test_id,
)
def test_get_dependency_value_error_cases(
    test_id: Literal["error-null-callable"], dependency: _Dependency, exception: type[ValueError]
) -> None:
    manager = DependenciesManager()

    with pytest.raises(exception):
        manager.get_dependency_value(dependency)


@pytest.mark.parametrize(
    "test_id, overrides, expected_old_overrides, expected_overrides_after_restore",
    [
        ("override-restore-no-previous", {mock_dependency_callable: mock_override_callable}, {}, {}),
        (
            "override-restore-with-previous",
            {mock_dependency_callable: mock_override_callable},
            {mock_dependency_callable: mock_dependency_callable},
            {mock_dependency_callable: mock_dependency_callable},
        ),
    ],
    ids=lambda test_id: test_id,
)
def test_override_restore_dependencies(
    test_id: Literal["override-restore-no-previous", "override-restore-with-previous"],
    overrides: OverridesMapping,
    expected_old_overrides: OverridesMapping,
    expected_overrides_after_restore: dict[Any, Any],
) -> None:
    manager = DependenciesManager()

    if test_id == "override-restore-with-previous":
        manager.override_dependencies({mock_dependency_callable: mock_dependency_callable})

    old_overrides = manager.override_dependencies(overrides)

    assert old_overrides == expected_old_overrides
    assert manager.dependency_overrides == overrides

    manager.restore_dependencies(overrides, old_overrides)

    assert manager.dependency_overrides == expected_overrides_after_restore
