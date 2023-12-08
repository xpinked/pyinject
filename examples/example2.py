from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Annotated

from typing_extensions import override

from pyinject import AutoWired, Depends, execute as _


class Country(Enum):
    US = auto()
    UK = auto()


class Employee:
    def __init__(self, name: str, country: Country, base_salary: float):
        self.name = name
        self.country = country
        self.base_salary = base_salary


class SalaryStrategy(ABC):
    @abstractmethod
    def calculate_salary(self, base_salary: float) -> float:
        pass


class USSalaryStrategy(SalaryStrategy):
    @override
    def calculate_salary(self, base_salary: float) -> float:
        return base_salary * 1.2


class UKSalaryStrategy(SalaryStrategy):
    @override
    def calculate_salary(self, base_salary: float) -> float:
        return base_salary * 1.1


class CalculateSalaryStrategyFactory:
    strategies = {
        Country.US: USSalaryStrategy(),
        Country.UK: UKSalaryStrategy(),
    }

    def get_strategy(self, country: Country) -> SalaryStrategy:
        if country in self.strategies:
            return self.strategies[country]

        raise ValueError(f"No salary strategy for country: {country}")


@AutoWired()
def calculate_employee_salary(
    employee: Employee,
    strategy_factory: Annotated[CalculateSalaryStrategyFactory, Depends()],
) -> float:
    strategy = strategy_factory.get_strategy(country=employee.country)
    return strategy.calculate_salary(employee.base_salary)


def main() -> None:
    employees = [
        Employee(name="Alice", country=Country.US, base_salary=1000),
        Employee(name="Bob", country=Country.UK, base_salary=2000),
    ]

    for emp in employees:
        salary = _(calculate_employee_salary, employee=emp)
        print(f"Salary for {emp.name} ({emp.country}): {salary}")


if __name__ == "__main__":
    main()
