# Supplementary Specification

## Request Field Requirements

All request fields shall adhere to the following requirements:

1. carPlate: non-empty string (not containing only whitespace).
2. rateName: non-empty string (not containing only whitespace).
3. cardData: non-empty string in 'n-c-mmyyyy' format, where:
   - 'n' is the card number (16 digits),
   - 'c' is the verification code (3 digits),
   - 'mmyyyy' is the expiration month and year (6 digits).
   - The credit card must not be expired (expiration date should be in the future).
4. euros: non-zero number, with up to 2 digits after the decimal point.
