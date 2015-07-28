import basset

my_user = basset.Contact()
my_user.add_name(given_name = "David",
                 family_name = "Wind",
                 full_name = "David Kofoed Wind")
my_user.add_email(address = "utdiscant@gmail.com")

basset.send_interaction(contact=my_user,
                        transaction_type="signup",
                        api_key="test")
