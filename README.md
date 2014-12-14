phishingfarm
============

Phishing Farm  
webserver.py is a tornado web server running at port 8000 which accepts 2 parameters.  
The tool rewrites all links in the webpage so that all traffic passes through this 'fake' web server.  
- uuid (unique identifier)
- url (base64 encoded string containing the full URL)    

Example:  
http://127.0.0.1:8000/query?uuid=931d7f60-65c4-01-d861-3c15c2ccadba&url=aHR0cDovL3d3dy50b3JuYWRvd2ViLm9yZy9lbi9icmFuY2gyLjEvLy8vaW50ZWdyYXRpb24uaHRtbA==

Upon base64 decoding, the parameter url translates to http://www.tornadoweb.org/en/branch2.1////integration.html.  

 
