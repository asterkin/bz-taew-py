# Use Case: Check Car

**Actors**: Parking Inspector

**Purpose**: Parking Inspector submits a request to check whether a car is legally parked.

**Overview**: This use case enables a Parking Inspector to check if a car is legally parked in a particular zone. The inspector submits the car's plate number and the zone, and the system returns the parking status.

**Additional Requirements**: [Supplementary Specification](./SupplementarySpecification.md)

## Typical course of events:

**Precondition**: Parking Rates per Zone are defined.

| Actor Action | System Response |
|:--------------|:----------------|
| 1. This use case begins when a Parking Inspector wants to check whether a car is leagally parked.| |
| 2. The Parking Inspector enters the car plate number and the zone to check. | 3. The system looks for a parking ticket associated with the car plate number and zone. |
|4. | The system returns the parking status and relevant description to the Parking Inspector. |

---

## Alternative Courses:

### Alternative Flow 1a: Parking Rates are Not Available (Preconditions Not Met)

| Actor Action | System Response |
|--------------|-----------------|
|  | 2a. The system returns a "The system is not ready: parking rates are not available. Please try again later." error message. |

---

### Alternative Flow 1b: Invalid Request Data

| Actor Action | System Response |
|:--------------|:----------------|
| 1a. The "Check Car" request contains invalid data. | 2a. The system rejects the request. |

The returned message depends on configuration and mode:
- In the case of an open API deployment available for integration with a 3rd party GUI developer,
    the message indicates either an integration mistake or a hacker attack.
- In the case of a complete full-stack deployment, the message indicates an implementation error.  

---

