# Use Case: Buy Ticket.

**Actors**: Car Driver, Payment Service

**Purpose**: Car Driver buys a parking ticket to avoid being fined.

**Overview**: This use case allows a Car Driver to purchase a parking ticket for a specific zone. The driver selects the zone, enters payment details, and receives a parking ticket upon successful payment.

**Additional Requirements**: [Supplementary Specification](./SupplementarySpecification.md)

## Typical course of events:

**Precondition**: Parking Rates per Zone are defined.

| Actor Action | System Response |
|:--------------|:----------------|
| 1. This use case begins when a Car Driver wants to purchase a parking ticket.| |
| 2. The Car Driver requests a list of available rates. | 3. The system returns the available rates. |
|4. The Car Driver selects a rate and submits a "buy a ticket" request with the amount of money to be paid and payment details.| The system sends a payment request to the Payment Service. |
|5. The Payment Service confirms the payment. | 6. The system calculates the allowed parking time, issues a parking ticket, and returns it to the car driver. |

**Postcondition**: The new parking ticket is stored within the system for further validation.

---

## Alternative Courses:

### Alternative Flow 2a: Parking Rates are Not Available (Preconditions Not Met)

| Actor Action | System Response |
|--------------|-----------------|
|  | 2a. The system returns a "The system is not ready: parking rates are not available. Please try again later." error message. |

---

### Alternative Flow 5a: Payment Declined

| Actor Action | System Response |
|:--------------|:----------------|
| 5a. The Payment Service declines the payment. | 6a. The system returns a "Credit Card was declined. Check the card number or use a different card." error message. |

**Postcondition**: No new ticket is saved within the system.

---

### Alternative Flow 5b: Payment Service is Unavailable

| Actor Action | System Response |
|:--------------|:----------------|
| 5b. The Payment Service is unavailable. | 6b. The system returns a "An error occurred while paying. Try it again later." error message. |

**Postcondition**: No new ticket is saved within the system.

---

### Alternative Flow 3c: Invalid Request Data

| Actor Action | System Response |
|:--------------|:----------------|
| 3c. The "Buy Ticket" request contains invalid data. | 4c. The system rejects the request. | 

The returned message depends on configuration and mode:
- In the case of an open API deployment available for integration with a 3rd party GUI developer,
    the message indicates either an integration mistake or a hacker attack.
- In the case of a complete full-stack deployment, the message indicates an implementation error.  

**Postcondition**: No payment request is sent, and no new ticket is saved within the system.

---
