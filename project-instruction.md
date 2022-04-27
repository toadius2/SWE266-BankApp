# Project Instruction

## Build Phase

### Course discussion for service and entity
#### Service for user service:
- edit user profile
- add transaction to transaction record (status: posted)
    - deposit
    - withdraw

#### Snapshot for bank account entity;
- accountId
- userId
- balance
- query balance by userId and accountId
- query transaction by userId and accountId

#### Snapshot for regular user entity(different snapshot for different roles like admin, manager):
- user profile (registration for user snapshot)
    - userId
    - username
    - userPassword
    - address
    - phoneNumber
    - email
    - transactionList
    - accountId

#### Snapshot for transaction entity:
- transactionId
- userId
- accountId
- transactionStatus: posted
- transactionTime: new Date()
- transactionName
- transactionAmount
