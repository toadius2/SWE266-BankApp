# Project Instruction

## Build Phase

### Course discussion for service and entity
#### Service for user service:
- edit user profile
    - (precondition) check if the user has an account
    - (postcondition) update user information
- add transaction to transaction record (status: posted)
    - deposit
        - (precondition) check if the user has an account
        - (precondition) The fractional input should match /[0-9]{2}/
        - (precondition) should match /(0|[1-9][0-9]*)/
        - (postcondition) update account amount
    - withdraw
        - (precondition) check if the user has an account
        - (precondition) balance >= amount
        - (precondition) The fractional input should match /[0-9]{2}/
        - (precondition) should match /(0|[1-9][0-9]*)/
        - (postcondition) update account amount
        

#### Snapshot for bank account entity;
- accountId (auto generated) (primary key)
- userId
- balance
    - (restriction) The fractional input should match /[0-9]{2}/
    - (restriction) should match /(0|[1-9][0-9]*)/
- query balance by userId and accountId
    - (precondition) check if the user has an account
    - (precondition) check if the user exists
    - (postcondition) get the balance
- query transaction by userId and accountId
    - (precondition) check if the user has an account
    - (precondition) check if the user exists
    - (postcondition) get the transaction

#### Snapshot for regular user entity(different snapshot for different roles like admin, manager):
- user profile (registration for user snapshot)
    - userId  (primary key)
    - username
        - (precondition) `/[_\\-\\.0-9a-z]/`
        - (precondition) between 1 and 127 characters long
    - userPassword
        - (precondition) `/[_\\-\\.0-9a-z]/`
        - (precondition) between 1 and 127 characters long
    - address
        - (precondition) U.S
    - phoneNumber
        - (precondition) only numbers without hyphen etc.
    - email
        - (precondition) email
    - transactionList
    - accountId

#### Snapshot for transaction entity:
- transactionId  (primary key)
- userId
- accountId
- transactionStatus: posted
- transactionTime: new Date()
- transactionName
- transactionAmount
    - (precondition) The fractional input should match /[0-9]{2}/
    - (precondition) should match /(0|[1-9][0-9]*)/
