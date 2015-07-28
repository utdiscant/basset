#!/usr/bin/env python
# -*- coding: utf-8 -*-

import basset

basset.apikey = "MEGALOL"

my_user = basset.User()
my_user.add_name(given_name="David", family_name="Wind", full_name="David Kofoed Wind")
my_user.add_email(address="utdiscant@gmail.com")
my_user.add_social_profile(site="facebook",
                           profile="davidwind")
my_user.add_phone(number="60 67 70 42",
                  country="DK")
my_user.add_postal_address(postal_address="Reventlowsgade 10, st. tv., 1651 København V")
my_user.add_credit_card(cardno="4571446721710990")

basset.compute_trust(user=my_user)
