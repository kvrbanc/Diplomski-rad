from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json

from bertsummarizer.summarizer_model import SummarizerModel


# Define the model
model = SummarizerModel()

# --------------------------------------------
#   Handler for the 'summarize' url path
# --------------------------------------------
@api_view(['POST',])
def summary_computation(request):

    # Check if the request body is provided
    if not request.data:
        return Response(
            data = {"detail": "Malformed request body. Body of the request is empty."},
            status = status.HTTP_400_BAD_REQUEST
        )

    # Get the request body
    req = request.data

    # Validate the names of the request parameters
    if not validateParameterNames(req):
        return Response(
            data = {"detail": "Malformed request body. Incorrect parameters provided. A set of correct parameters: \"text\", \"numOfSents\", \"sentRatio\", \"useFirstSent\". "},
            status = status.HTTP_400_BAD_REQUEST
        )
    
    # Check if the parameter *text* is provided
    if "text" not in req.keys():
        return Response(
            data = {"detail": "Malformed request body. Body of the request must contain a \"text\" parameter."},
            status = status.HTTP_400_BAD_REQUEST
        )
    
    # Extract the values of the request parameters (if there is no value, use the default value)
    content = req["text"]
    numberOfSentences = req.get("numOfSents", None)
    sentenceRatio = req.get("sentRatio", 0.2)
    useFirstSent = req.get("useFirstSent", True)

    # Validate the types of the request parameters
    error_message, request_parameters = validateParameterTypes(content, numberOfSentences, sentenceRatio, useFirstSent)
    if error_message:
        return Response(
            data = {"detail": error_message},
            status = status.HTTP_400_BAD_REQUEST
        )
    
    # Extract the parameter values (this is used in case there is a  'application/x-www-form-urlencoded' type body, 
    # where all the parameter values are strings)
    content = request_parameters["text"]
    numberOfSentences = request_parameters["numOfSents"]
    sentenceRatio = request_parameters["sentRatio"]
    useFirstSent = request_parameters["useFirstSent"]
    
    # Validate the value range of the provided request parameters 
    # -- since the *useFirstSent* is a boolean, it doesn't have to be validated
    error_message = validateValueRange(content, numberOfSentences, sentenceRatio)
    if error_message:
        return Response(
            data = {"detail": error_message},
            status = status.HTTP_400_BAD_REQUEST
        )
 
    # Use the model to make a summary
    summary = model(content=content , sent_ratio=sentenceRatio, num_sentences=numberOfSentences, use_first_sent=useFirstSent)

    # Return a response containing the summary  
    return Response(
        data={"content":summary}
    )
    

# ---------------------------------------------------------
#   Function for checking parameter names of a request body
# ---------------------------------------------------------
def validateParameterNames(requestBody):

    # A set of valid parameter names
    valid_parameters = ["text", "numOfSents", "sentRatio", "useFirstSent"]

    # Extract the body's parameter names and check if they are valid
    request_parameters = requestBody.keys()
    if set(request_parameters).issubset(set(valid_parameters)):
        return True
    else:
        return False


# ---------------------------------------------------------
#   Function for checking parameter value types 
# ---------------------------------------------------------
def validateParameterTypes(content, numberOfSentences, sentenceRatio, useFirstSentence ):

    error_message = "Malformed request body. "
    request_parameters = {}

    # Check if the value of the "text" parameter is a string
    if not type(content) == str:
        return (error_message + "The parameter \"text\" must have a string value.", None)
    request_parameters["text"] = content
    
    # If provided, check if the value of the "numOfSents" parameter is a integer
    #  - It could be sent as a string, so try to convert it to integer
    if numberOfSentences is not None:
        if type(numberOfSentences) != int:
            if type(numberOfSentences) == str:
                try:
                    numberOfSentences = int(numberOfSentences)
                except ValueError:
                    return (error_message + "The parameter \"numOfSents\" must have an integer value.", None)
            else:
                return (error_message + "The parameter \"numOfSents\" must have an integer value.", None)
    request_parameters["numOfSents"] = numberOfSentences

    # Check if the value of the "sentRatio" parameter is a float
    #  - It could be sent as a string, so try to convert it to float
    if type(sentenceRatio) != float:
        if type(sentenceRatio) == str:
            try:
                sentenceRatio = float(sentenceRatio)
            except ValueError:
                return (error_message + "The parameter \"sentRatio\" must have a float value.", None)
        else:
            return (error_message + "The parameter \"sentRatio\" must have a float value.", None)
    request_parameters["sentRatio"] = sentenceRatio

    # Check if the value of the "useFirstSent" parameter is a boolean
    #  - It could be sent as a string, so try to convert it to boolean
    if type(useFirstSentence) != bool:
        if type(useFirstSentence) == str:
            if useFirstSentence.lower() == "true":
                useFirstSentence = True
            elif useFirstSentence.lower() == "false":
                useFirstSentence = False
            else:
                return (error_message + "The parameter \"useFirstSent\" must have a boolean value.", None)
        else:
            return (error_message + "The parameter \"useFirstSent\" must have a boolean value.", None)
    request_parameters["useFirstSent"] = useFirstSentence
    
    return (False, request_parameters)


# ---------------------------------------------------------
#   Function for checking if the parameter values are
#   in the appropriate range.
# ---------------------------------------------------------
def validateValueRange(content, numberOfSentences, sentenceRatio):

    # Define the error message
    error_message = "Malformed request body. "

    # Check if the *content* is of an appropriate length (more than 40 characters)
    if len( content ) < 41:
        return error_message + "The value of the \"text\" parameter is too short (below 41 characters)."
    
    # Check if *content* contains more than one word
    if len( content.split() ) == 1:
        return error_message + "The value of the \"text\" parameter contains only one word."
    
    # Check if *numberOfSentences* (if provided) is in the [1 - 999] range
    if numberOfSentences is not None:
        if not ( numberOfSentences >= 1 and numberOfSentences <= 999 ):
            return error_message + "The value of the \"numOfSents\" parameter is not in the [1 - 999] range."
    
    # Check if *sentenceRatio* is in the [0.05 - 1.0] range
    if not ( sentenceRatio >= 0.05 and sentenceRatio <= 1.0 ):
        return error_message + "The value of the \"sentRatio\" parameter is not in the [0.05 - 1.0] range."

    # If there is no error, return false
    return False
    
        