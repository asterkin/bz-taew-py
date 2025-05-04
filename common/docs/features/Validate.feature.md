`@Validate`
# Feature: Strict Validation of all Request Fields

**Requirements**: [Supplimenetary Specification](../use-cases/SupplementarySpecification.md)

## Scenario Outline: Validate request fields
  * Given the current datetime is "2024/07/02 17:30"
  * When this '<field>' field has this '<value>' value
  * Then this '<error>' error is returned

### Examples:

  | field    | value                       | error                                                                                                  |
  | -------- | --------------------------- | ------------------------------------------------------------------------------------------------------ |
  | carPlate |                             | Car plate must be provided                                                                             |
  | rateName |                             | Rate must be provided                                                                                  |
  | euros    | 0                           | Euros value must be non-zero                                                                           |
  | euros    | -1.5                        | Euros value must be non-zero                                                                           |
  | euros    | 1.753                       | Euros value must have up to 2 digits after the decimal point                                           |
  | card     |                             | Card data must be provided                                                                             |
  | card     | 1234                        | "Card data (1234) must be in the format 'n-c-mmyyyy', where 'n' is the card number (16 digits), 'c' is the verification code (3 digits), and 'mmyyyy' is the expiration month and year (6 digits)" |
  | card     | 1234567890123456-123-062023 | Card expiration month and year (062023) must be equal to or after the current month and year (072024)  | 
  | card     | 1234567890123456-123-062024 | Card expiration month and year (062024) must be equal to or after the current month and year (072024)  |
