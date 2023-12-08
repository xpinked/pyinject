from dataclasses import dataclass
from typing import Annotated

from pyinject import AutoWired, Depends, execute


@dataclass
class Employee:
    name: str
    age: int


class EmployeeRepository:
    def get_employee(self) -> Employee:
        return Employee("John", 30)


class EmployeeBirthdayService:
    def send_happy_birthday(self, employee: Employee) -> None:
        print(f"Happy birthday {employee.name}!")

    def get_employee_age(self, employee: Employee) -> int:
        return employee.age


class EmployeeService:
    """
    Employee Service
    """

    @AutoWired()
    def __init__(
        self,
        _employee_repository: Annotated[EmployeeRepository, Depends()],
        _employee_birthday_service: Annotated[EmployeeBirthdayService, Depends()],
    ) -> None:
        self._employee_repository = _employee_repository
        self._employee_birthday_service = _employee_birthday_service

    def get_employee(self) -> Employee:
        return self._employee_repository.get_employee()


@AutoWired()
def main(
    employee_service: Annotated[EmployeeService, Depends()],
    employee_birthday_service: Annotated[EmployeeBirthdayService, Depends()],
) -> None:
    employee = employee_service.get_employee()
    print(employee_birthday_service.get_employee_age(employee))
    employee_birthday_service.send_happy_birthday(employee)


if __name__ == "__main__":
    # normal Dependency injection configuration
    employee_repository = EmployeeRepository()
    employee_birthday_service = EmployeeBirthdayService()

    employee_service = EmployeeService(
        _employee_repository=employee_repository,
        _employee_birthday_service=employee_birthday_service,
    )

    main(
        employee_service=employee_service,
        employee_birthday_service=employee_birthday_service,
    )

    # pyinject injection - no need to configure dependencies, it will be done automatically
    execute(starting_point=main)
