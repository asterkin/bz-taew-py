# Use Case: Define Parking Rates

**Actors**: Administrator

**Purpose**: The Administrator defines parking rates for different zones in the system.

**Overview**: This use case allows an Administrator to set or update the parking rates for specific zones. The Administrator provides the rate details, and the system stores these rates for use in ticket purchases.

**Additional Requirements**: [Supplementary Specification](./SupplementarySpecification.md)

## Typical course of events:

**Precondition**: The system is operational, and the Administrator is authenticated.

| Actor Action | System Response |
|:--------------|:----------------|
| 1. This use case begins when an Administrator wants to define or update parking rates.| |
| 2. The Administrator submits a request to define or update all parking rates for available zones. | 3. The system validates the request and stores the new or updated rates. |
|  | 4. The system returns a confirmation to the Administrator. |

**Postcondition**: The new or updated parking rates are stored within the system and available for use in ticket purchases.

---

## Alternative Courses:

### Alternative Flow 2a: Invalid Rate Data

| Actor Action | System Response |
|--------------|-----------------|
| 2a. The Administrator submits invalid rate data. | 3a. The system rejects the request and returns an error message indicating the invalid data. |

**Postcondition**: No new or updated rates are saved within the system.

---

### Alternative Flow 2b: System Error

| Actor Action | System Response |
|:--------------|:----------------|
| 2b. The system encounters an error while processing the request. | 3b. The system returns an error message and logs the issue for further investigation. |

**Postcondition**: No new or updated rates are saved within the system.

---
