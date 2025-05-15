`@world.ForParkingInspectors`
# Feature: Check Car Parking Status

**Use Case**: [Check Car](../use-cases/CheckCar.md)

## Background:
  * Given the existing parking rates per zone are

    | name   | eurosPerHour |
    | ------ | ------------ |
    | Blue   | 0.80         |
    | Green  | 0.85         |
    | Orange | 0.75         |

  * And the following tickets are stored in the system

    | ticketCode | carPlate | rateName | startingDateTime | endingDateTime   | price |
    | ---------- | -------- | -------- | ---------------- | ---------------- | ----- |
    | 1234567890 | 6989GPJ  | Green    | 2024/01/02 17:00 | 2024/01/02 19:00 | 1.70  |
    | 1234567892 | XYZ7890  | Orange   | 2024/01/02 15:00 | 2024/01/02 17:00 | 1.50  |

  * And the current datetime is "2024/01/02 17:30"

## Scenario Outline: Check car parking status - Main Flow
  * When the Parking Inspector submits the car plate '<carPlate>' and the rate name '<rateName>'
  * Then no error should be thrown
  * And the system responds with the status '<legallyParked>'

### Examples:

  | carPlate | rateName | legallyParked |
  | -------- | -------- | ------------- |
  | 6989GPJ  | Green    | True          |
  | XYZ7890  | Orange   | False         |
  | 6989GPJ  | Blue     | False         |
  | 6989GPK  | Green    | False         |

## Scenario: Check car parking status - Exceptional Flow (invalid rate name)

**Note**: This scenario covers the most important case of an invalid request (invalid rate name). Other cases of invalid requests will be covered by the [Validatate](./Validate.feature.md) tests.

  * When the Parking Inspector submits the car plate '6989GPJ' and the rate name 'Black'
  * Then this 'Rate with name "Black" not found' error is returned

## Scenario: Preconditions are Not Met (step 2a)
  * Given no parking rates per zone defined
  * When the Parking Inspector submits the car plate '6989GPJ' and the rate name 'Green'
  * Then this 'The system is not ready: parking rates are not available. Please try again later.' error is returned

