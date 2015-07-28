Feature: Test conversion of contacts between different formats
    Scenario: Test conversion between Contact and JSON
        Given we have a contact mapper from Contact to JSON
        When we input a contact in Contact format into the converter
        And we convert it back again
        Then we get the original contact back