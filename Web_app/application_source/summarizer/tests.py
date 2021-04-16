from django.test import TestCase, Client
import json

class ApiTest(TestCase):

    # Define the variables before the testing starts
    def setUp(self):

        # The 'client' that will be used to send requests
        self.client = Client()

        # Text used to test summary computation
        self.textToSummarize = '''
        Most of the solar system's asteroids live and work in the main asteroid belt, a roughly flat zone between the orbits of Mars and Jupiter.
        By tradition, the discoverers get to name their asteroids whatever they like.
        Often drawn by artists as a region of cluttered, meandering rocks in the plane of the solar system, the asteroid belt's total mass is less than five percent that of the Moon, which is itself barely more than one percent of Earth's mass.
        Sounds insignificant.
        But accumulated perturbations of their orbits continually create a deadly subset, perhaps a few thousand, whose eccentric paths intersect Earth's orbit.
        A simple calculation reveals that most of them will hit Earth within a hundred million years.
        The ones larger than about a kilometer across will collide with enough energy to destabilize Earth's ecosystem and put most of Earth's land species at risk of extinction.
        That would be bad.
        Asteroids are not the only space objects that pose a risk to life on Earth.
        The Kuiper belt is a comet-strewn swath of circular real estate that begins just beyond the orbit of Neptune, includes Pluto, and extends perhaps as far again from Neptune as Neptune is from the Sun.
        The Dutch-born American astronomer Gerard Kuiper advanced the idea that in the cold depths of space, beyond the orbit of Neptune, there reside frozen leftovers from the formation of the solar system.
        Without a massive planet upon which to fall, most of these comets will orbit the Sun for billions more years.
        As is true for the asteroid belt, some objects of the Kuiper belt travel on eccentric paths that cross the orbits of bonafide planets.
        Pluto and its ensamble of siblings called Plutinos cross Neptune's path around the Sun.
        Other Kuiper belt objects plunge all the way down to the inner solar system, crossing planetary orbits with abandon.
        This subset includes Halley, the most famous comet of them all.
        Far beyond the Kuiper belt, extending halfway to the nearest stars, lives a spherical reservoir of comets called the Oort cloud, named for Jan Oort, the Dutch astrophysicist who first deducted its existence.
        This zone is responsible for the long-period comets, those with orbital periods far longer than a human lifetime.
        Unlike Kuiper belt comets, Oort cloud comets can rain down on the inner solar system from any angle and from any direction.
        The two brightest of the 1900s, comets Hale-Bopp and Hyakutake, were both from the Oort cloud and are not coming back anytime soon.
        '''

        # Expected summary of above text
        self.expectedSummary = "Most of the solar system's asteroids live and work in the main asteroid belt, a roughly flat zone between the orbits of Mars and Jupiter. By tradition, the discoverers get to name their asteroids whatever they like. The ones larger than about a kilometer across will collide with enough energy to destabilize Earth's ecosystem and put most of Earth's land species at risk of extinction. As is true for the asteroid belt, some objects of the Kuiper belt travel on eccentric paths that cross the orbits of bonafide planets. This subset includes Halley, the most famous comet of them all. Far beyond the Kuiper belt, extending halfway to the nearest stars, lives a spherical reservoir of comets called the Oort cloud, named for Jan Oort, the Dutch astrophysicist who first deducted its existence. Unlike Kuiper belt comets, Oort cloud comets can rain down on the inner solar system from any angle and from any direction."

    
    # Send a request with the body of an unsupported type -- *text/plain*
    def test_unsupported_media_type(self):

        # Define the request body and send the request
        request_body = "Some random text ..."
        response = self.client.post( path = '/summarize' , data = request_body , content_type="text/plain" )

        self.assertEqual (response.status_code , 415)


    # Send a request with an empty body
    def test_empty_request_body(self):
        
        # Define the request body and send the request
        request_body = {}
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. Body of the request is empty.")


    # Send a request with a body containing an incorrect parameter name
    def test_incorrect_parameter_name(self):

        # Define the request body and send the request
        request_body = {
            "text" : "Placeholder text.",
            "numOfSents" : 1,
            "randomParameter": 1.3
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. Incorrect parameters provided. A set of correct parameters: \"text\", \"numOfSents\", \"ratio\", \"useFirstSent\". ")
    

    # Send a request with a body lacking the *text* parameter (which is required)
    def test_missing_text_parameter(self):
        
        # Define the request body and send the request
        request_body = {
            "numOfSents" : 3,
            "sentRatio" : 0.2,
            "useFirstSent": True
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. Body of the request must contain a \"text\" parameter.")
    

    # Send a request with a body containing a parameter *numOfSents* with a value of an incorrect type
    def test_incorrect_parameter_type_1(self):

        # Define the request body and send the request
        request_body = {
            "text" : "Text content.",
            "numOfSents" : "Three",
            "sentRatio" : 0.2,
            "useFirstSent": True
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. The parameter \"numOfSents\" must have an integer value.")
    

    # Send a request with a body containing a parameter *sentRatio* with a value of an incorrect type
    def test_incorrect_parameter_type_2(self):

        # Define the request body and send the request
        request_body = {
            "text" : "Text content.",
            "numOfSents" : 6,
            "sentRatio" : "zero point two",
            "useFirstSent": True
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. The parameter \"sentRatio\" must have a float value.")


    # Send a request with a body containing a parameter *useFirstSent* with a value of an incorrect type
    def test_incorrect_parameter_type_3(self):

        # Define the request body and send the request
        request_body = {
            "text" : "Text content.",
            "numOfSents" : 6,
            "sentRatio" : 0.2,
            "useFirstSent": "Use it"
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. The parameter \"useFirstSent\" must have a boolean value.")


    # Send a request with a body containing a parameter *text* with a value of an incorrect type
    def test_incorrect_parameter_type_4(self):

        # Define the request body and send the request
        request_body = {
            "text" : 12345,
            "numOfSents" : 6,
            "sentRatio" : 0.2,
            "useFirstSent": True
        }
        response = self.client.post( path = '/summarize' , data = request_body , content_type="application/json")

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. The parameter \"text\" must have a string value.")


    # Send a request with a body containing a parameter *text* with value in the incorrect range (too short)
    def test_incorrect_value_range_1(self):

        # Define the request body and send the request
        request_body = {
            "text" : "Random text.",
            "numOfSents" : 6,
            "sentRatio" : 0.2,
            "useFirstSent": False
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. The value of the \"text\" parameter is too short (below 41 characters).")
    

    # Send a request with a body containing a parameter *numOfSents* with value in the incorrect range
    def test_incorrect_value_range_2(self):

        # Define the request body and send the request
        request_body = {
            "text" : self.textToSummarize,
            "numOfSents" : 1024,
            "sentRatio" : 0.2,
            "useFirstSent": False
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. The value of the \"numOfSents\" parameter is not in the [1 - 999] range.")


    # Send a request with a body containing a parameter *sentRatio* with a value in the incorrect range
    def test_incorrect_value_range_3(self):

        # Define the request body and send the request
        request_body = {
            "text" : self.textToSummarize,
            "numOfSents" : 6,
            "sentRatio" : 1.25,
            "useFirstSent": False
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 400)
        self.assertEqual (json.loads(response.content)["detail"], "Malformed request body. The value of the \"sentRatio\" parameter is not in the [0.05 - 1.0] range.")


    # Send a correctly formatted request and check the calculated summary
    def test_summary_computation(self):

        # Define the request body and send the request
        request_body = {
            "text" : self.textToSummarize,
            "numOfSents" : 6,
            "useFirstSent": True
        }
        response = self.client.post( path = '/summarize' , data = request_body )

        self.assertEqual (response.status_code , 200)
        self.assertEqual (json.loads(response.content)["content"], self.expectedSummary )