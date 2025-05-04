`@ForParkingCars`
# Feature: Support Parking Zone-Based Pricing with Credit Card Payments

**Use Case**: [Buy Ticket](../use-cases/BuyTicket.md)

## Background:

  * Given the existing parking rates per zone are

    | name   | eurosPerHour |
    | ------ | ------------ |
    | Blue   | 0.80         |
    | Green  | 0.85         |
    | Orange | 0.75         |

  * And the next ticket code is 1234567890
  * And the current datetime is "2024/01/02 17:00"
  * And no tickets are stored in the system

## Scenario: Obtain parking rates (steps 1-2)
  * When the Car Driver submits a "get available rates" request
  * Then no error should be thrown
  * And all available parking rates per zone are returned

    | name   | eurosPerHour |
    | ------ | ------------ |
    | Blue   | 0.80         |
    | Green  | 0.85         |
    | Orange | 0.75         |

## Scenario: Buy ticket main flow (steps 3-6)
  * And the Payment Service will accept the payment request
  * When the Car Driver submits this "buy ticket" request

    | carPlate | rateName | euros | card                        |
    | -------- | -------- | ----- | --------------------------- |
    | 6989GPJ  | Green    | 1.70  | 1234567890123456-123-062027 |

  * Then no error should be thrown
  * And this "pay request" is submitted to the Payment Service

    | euros | card                        |
    | ----- | --------------------------- |
    | 1.70  | 1234567890123456-123-062027 |

  * And this ticket is returned

    | ticketCode | carPlate | rateName | startingDateTime | endingDateTime   | price | paymentId    |
    | ---------- | -------- | -------- | ---------------- | ---------------- | ----- | ------------ |
    | 1234567890 | 6989GPJ  | Green    | 2024/01/02 17:00 | 2024/01/02 19:00 | 1.70  | <paymentId>  |

  * And the ticket is stored with ticketCode '1234567890'

## Scenario Outline: Buy ticket exceptions - a payment error (steps 5a,b-6a,b)
  * And the Payment Service will respond with a <payment error> error
  * When the Car Driver submits this "buy ticket" request

    | carPlate | rateName | euros | card                        |
    | -------- | -------- | ----- | --------------------------- |
    | 6989GPJ  | Green    | 1.70  | 1234567890123456-123-062027 |

  * Then this '<error message>' error is returned
  * And no ticket with the ticketCode '1234567890' is stored

### Examples:

  | payment error          | error message                                                            |
  | ---------------------- | ------------------------------------------------------------------------ |
  | "Credit Card Declined" | Credit Card was declined. Check the card number or use a different card. |
  | "System Error"         | An error occurred while paying. Try it again later.                      |

## Scenario: Buy ticket exceptions - invalid request data (steps 3c-4c)

**Note**: This scenario covers the most important case of an invalid request (invalid rate name). Other cases of invalid requests will be covered by the [Validatate](./Validate.feature.md) tests.

  * And the Payment Service will accept the payment request
  * When the Car Driver submits this "buy ticket" request

    | carPlate | rateName | euros | card                        |
    | -------- | -------- | ----- | --------------------------- |
    | 6989GPJ  | Black    | 1.70  | 1234567890123456-123-062027 |

  * Then this 'Rate with name "Black" not found' error is returned
  * And no request is submitted to the Payment Service
  * And no ticket with the ticketCode '1234567890' is stored

## Scenario: Preconditions are Not Met (step 2a)
  * And no parking rates per zone defined
  * When the Car Driver submits a "get available rates" request
  * Then this 'The system is not ready: parking rates are not available. Please try again later.' error is returned

