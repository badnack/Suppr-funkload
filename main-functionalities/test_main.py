# -*- coding: iso-8859-15 -*-
"""Simple FunkLoad test
$Id$
"""
import unittest
import datetime
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.utils import extract_token
from funkload.Lipsum import Lipsum


class Main(FunkLoadTestCase):
    """This test use a configuration file Simple.conf."""

    def setUp(self):
      """Setting up test."""
      self.server_url = self.conf_get('main', 'url')

    def test_main_path(self):
	server_url = self.server_url
        # create a new user
	self.get(server_url, description='Get root URL')
	self.get(server_url + "/users/sign_up", description="View the user signup page")
	auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')
	email = Lipsum().getUniqWord() + "@" + Lipsum().getWord() + ".com"
	first_name = Lipsum().getWord()
	last_name = Lipsum().getWord()
	self.post(self.server_url + "/users",
	    params=[['user[email]', email],
                    ['user[first_name]', first_name],
                    ['user[last_name]', last_name],
                    ['user[password]', 'alphabet'],
                    ['user[password_confirmation]', 'alphabet'],
                    ['authenticity_token', auth_token],
                    ['commit', 'Sign up']],
                  description="Create New User")


        # create a new suppr
	self.get(server_url + "/dinners/new", description="Create a new suppr")
	auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')
	suppr_title = Lipsum().getSentence()
        suppr_date = datetime.date.today() + datetime.timedelta(days=10)
        suppr_location = Lipsum().getSentence()
        suppr_description = Lipsum().getSentence()
        suppr_category = "Italian"
        suppr_price = 26
        suppr_seats = 30
        # FIXME: suppr_image ....
	self.post(self.server_url + "/dinners",
                  params=[['dinner[title]', suppr_title],
                          ['dinner[date]', suppr_date],
                          ['dinner[location]', suppr_location],
                          ['dinner[description]', suppr_description],
                          ['dinner[price]', suppr_price],
                          ['dinner[category]', suppr_category],
                          ['dinner[seats]', suppr_seats],
                          ['authenticity_token', auth_token],
                          ['commit', 'Create Dinner']],
                  description="Create New Suppr")
	last_url = self.getLastUrl()
	created_suppr_id = last_url.split('/')[-1]

        # edit the suppr just created
        self.get(server_url + "/dinners/" + created_suppr_id + "/edit", description="Create a new suppr")
        auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')        
        suppr_date = datetime.date.today() + datetime.timedelta(days=2)
        self.post(self.server_url + "/dinners",
                  params=[['dinner[title]', suppr_title],
                          ['dinner[date]', suppr_date],
                          ['dinner[location]', suppr_location],
                          ['dinner[description]', suppr_description],
                          ['dinner[price]', suppr_price],
                          ['dinner[category]', suppr_category],
                          ['dinner[seats]', suppr_seats],
                          ['authenticity_token', auth_token],
                          ['commit', 'Create Dinner']],
                  description="Edit the created Suppr")

        # add a comment
	self.get(server_url + "/dinners/"+created_suppr_id, description="View the created Suppr page")
	auth_token = extract_token(self.getBody(), 'name="authenticity_token" type="hidden" value="', '"')
        comment_content = Lipsum().getSentence()
        comment_suppr_id = extract_token(self.getBody(), 'id="comment_dinner_id" name="comment[dinner_id]" type="hidden" value="', '"')
        self.post(self.server_url + "/comments",
                  params=[['comment[content]', comment_content],
                          ['comment[dinner_id]', comment_suppr_id],
                          ['authenticity_token', auth_token],
                          ['commit', 'Create Comment']],
                  description="Create New Comment")



    def test_main_path_readonly(self):
	server_url = self.server_url
	self.get(server_url, description='View root URL')
	self.get(server_url + "/users/sign_up", description="View the user signup page")
	self.get(server_url + "/users/sign_up", description="View the user signup page")
	self.get(server_url + "/home/about", description="View the user signup page")



if __name__ in ('main', '__main__'):
  unittest.main()
