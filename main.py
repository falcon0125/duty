#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# USERLIST DB = 'USERLIST'
# DUTY_TABLE = 'DUTY_TABLE'


class Userlist(ndb.Model):
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class Duty_table(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class events_handler(webapp2.RequestHandler):
    def post(self):
        db = Duty_table(parent=ndb.Key('DUTY_TABLES', 'default'))
        db.content = self.request.get('content')
        db.put()
        self.response.write('ok ' + repr(self.request.get("content")))

    def get(self):
        dutytableQ = Duty_table.query(ancestor=ndb.Key('DUTY_TABLES', 'default')).order(-Duty_table.date)
        duty_table = dutytableQ.fetch(1)
        self.response.write(duty_table[0].content)


class users_handler(webapp2.RequestHandler):
    def post(self):
        db = Userlist(parent=ndb.Key('USERLIST', 'default'))
        db.content = self.request.get('content')
        db.put()
        self.response.write('ok ' + repr(self.request.get("content")))

    def get(self):
        USERSQ = Userlist.query(ancestor=ndb.Key('USERLIST', 'default')).order(-Userlist.date)
        users = USERSQ.fetch(1)
        self.response.write(users[0].content)


app = webapp2.WSGIApplication([
                                  ('/', MainHandler), ('/events', events_handler), ('/users', users_handler)
                              ], debug=True)
