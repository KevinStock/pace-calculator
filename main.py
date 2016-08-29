#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

template_dir = os.path.join(
    os.path.dirname(__file__),
    "templates"
)

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir), autoescape = True
)

events = [("Marathon", 26.219), ("Half-Marathon", 13.1094), ("10K", 6.21371), ("5K", 3.10686)]

def time_to_seconds(hours, minutes, seconds):
    total_seconds = seconds
    if minutes > 0:
        total_seconds += minutes * 60
    if hours > 0:
        total_seconds += hours * 2600
    return total_seconds

def km_to_miles(km):
    return km * .62137

def seconds_to_pace(total_seconds):
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return str(minutes) + " minutes and " + str(seconds) + " seconds."



class MainHandler(webapp2.RequestHandler):
    def get(self):
        t_form = jinja_env.get_template("form.html")
        main_content = t_form.render(events = events)
        response = main_content
        self.response.write(response)
    
    def post(self):
        time_hours = int(self.request.get("time_hours"))
        time_minutes = int(self.request.get("time_minutes"))
        time_seconds = int(self.request.get("time_seconds"))
        distance = float(self.request.get("distance"))
        unit = self.request.get("unit")
        event = self.request.get("event")
        pace_hours = int(self.request.get("pace_hours"))
        pace_minutes = int(self.request.get("pace_minutes"))
        pace_seconds = int(self.request.get("pace_seconds"))
        
        time_total_seconds = time_to_seconds(time_hours, time_minutes, time_seconds)
        
        if distance != "":
            if unit == "kilometer":
                distance_miles = km_to_miles(distance)
            else:
                distance_miles = distance
        
        pace_total_seconds = time_total_seconds / distance_miles
        
        self.response.write(str(pace_total_seconds) + "<br />" + seconds_to_pace(pace_total_seconds))

        
class PaceHandler(webapp2.RequestHandler):
    def get(self):
        pace_seconds = self.request.get("pace_seconds")
        self.response.out.write(pace_seconds)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/pace', PaceHandler)
], debug=True)
