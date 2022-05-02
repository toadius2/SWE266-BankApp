# Project Information

## Test Oracle

- Scenario: valid registration

```bash=
Given the username, password, and initial balance are all valid
 When I register with the above valid input  
 Then an account under the username should be opened with the initial balance
```

- Scenario: invalid registration
```bash=
Given one or more of the username, password, and initial balance are invalid
 When I register with the above valid input
 Then "invalid_input" should be shown on screen 
  And no account should be opened
```

- Scenario: failed login
```bash=
Given the username or password are nonexistent or incorrect
 When I log in to the bank with the above invalid input
 Then the login should fail
```

- Scenario: authorized deposit
```bash=
Given I am a registered customer
 When I successfully log in to the bank with my username and password
  And I deposit with a valid amount
 Then I should know the deposit is successful
  And I should see my current balance after the deposit
```

- Scenario: authorized and valid withdrawal
```bash=
Given I am a registered customer
 When I successfully log in to the bank
  And I withdraw an amount smaller or equal to my current balance
 Then I should know the withdrawal is successful
  And I should see my current balance after the withdrawal
```

- Scenario: authorized and invalid withdrawal
```bash=
Given I am a registered customer
 When I successfully log in to the bank
  And I withdraw an amount larger than my current balance
 Then I should know the withdrawal is failed
Scenario: authorized balance query
```

- Given I am a registered customer
```bash=
 When I successfully log in to the bank
  And I check my balance
 Then I should see my current balance
```