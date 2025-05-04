# Acceptance Tests for BlueZone Application

This folder contains the [Gherkin](https://cucumber.io/docs/gherkin/reference/) specifications for the acceptance tests of the BlueZone application. These tests are designed to validate the behavior of the BlueZone application in various real-world scenarios to ensure that it meets its functional requirements.

## Overview

The acceptance tests cover the core use cases of the BlueZone application by simulating user interactions and verifying the expected outcomes. These tests are written in [Gherkin](https://cucumber.io/docs/gherkin/reference/) language, which allows for clear and human-readable test scenarios.

## Note on Test Coverage

A separate acceptance test for the ["Define Parking Rates"](../use-cases/DefineParkingRates.md) use case is not provided here, as this functionality is indirectly validated by the tests for the ["Buy Ticket"](../use-cases/BuyTicket.md) and ["Check Car"](../use-cases/CheckCar.md) use cases. The system's ability to define and update parking rates is critical for these two use cases, and their acceptance tests thoroughly cover scenarios that require defined parking rates.

## List of Acceptance Tests

| Test File                           | Description                                                                                       |
|-------------------------------------|---------------------------------------------------------------------------------------------------|
| [BuyTicket](./BuyTicket.feature.md) | Validates the process of purchasing a parking ticket by a Car Driver.                             |
| [CheckCar](./CheckCar.feature.md)   | Verifies the actions taken by a Parking Inspector to check parked cars and enforce parking rules. |
| [Validate](./Validate.feature.md)   | Separate test for input data validation.                                                          |

---

For more details about the BlueZone sample application, please refer to the [README.md](../../README.md) file in the root directory.