Feature: Testing the API endpoints

    Scenario: Test the /get/info endpoint of the API
        Given we have the testing database
        When we query the api endpoint '/get/info' with
        '''
        {
            "email" : [
                {
                    "address" : "pa@dit.dk",
                    "label" : "other"
                }
            ],
            "name" : [
                {
                    "givenName" : "Per",
                    "fullName" : "Per Andersen",
                    "familyName" : "Andersen"
                }
            ]
        }
        '''
        Then the API will return a string