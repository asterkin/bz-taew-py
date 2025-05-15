# Glossary

This glossary consolidates key terms used throughout the **BlueZone Application** documentation to ensure consistent usage and understanding.

---

## General Terms

- **Actor**: A person, organization, or system (including operating system–provided services) that interacts with the application to achieve a specific goal. In BlueZone, the primary actors are Car Driver, Parking Inspector, Administrator, and the System Clock.

- **Use Case**: A specific, goal-driven interaction between an actor and the system. Use cases define functional behavior and form the basis for acceptance criteria and architectural boundaries.

- **Ticket**: A digital confirmation that grants parking rights to a Car Driver for a specific zone and time range.

- **Zone**: A designated parking area within a city where specific rates and parking rules apply.

---

## System-Specific Terms

- **Car Driver**: An end user who uses the application to pay for parking in regulated city zones.

- **Parking Inspector**: A city official who uses the application to check whether a car is legally parked.

- **Administrator**: A user with elevated privileges responsible for defining and updating parking rates in different zones.

- **Parking Rate**: The cost per unit of time for parking in a specific zone. Managed by the Administrator.

- **Parking Status**: The system-determined state of a car in a particular zone—legal or illegal—based on existing tickets.

- **System Clock**: An external time source provided by the operating system or environment. It is treated as an actor when the application depends on it for current time values (e.g., calculating expiration times or scheduling actions). Although not a user-driven system, it represents an immutable dependency outside the application's control.

---

## Technical Terms

- **Adapter**: A software component that interfaces between the core application and external systems (e.g., databases, messaging services). Adapters implement the specific protocols defined by ports in the core logic.

- **Port**: A collection of abstract interfaces (preferably using language-native Protocols) that defines how the core application interacts with external systems or actors. Ports represent the extension points of the core logic.

- **Strategy**: A design pattern used to encapsulate a family of algorithms or behaviors, allowing them to be selected or swapped at runtime without modifying the core logic.

- **Component Plus Strategy**: An architectural approach used to modularize internal logic or adapter implementations, enabling flexible algorithm selection while maintaining a clean separation of concerns.

- **Feature**: In the context of Gherkin and Cucumber, a *feature* represents a high-level specification of a system behavior, typically mapping to a use case.

- **World**: A runtime context object used during Cucumber execution to hold shared state, dependencies, and references across test steps.

- **Tag**: A Gherkin annotation (e.g., `@fast`, `@admin`) used to categorize, filter, or control the execution of scenarios and features in acceptance tests.

---