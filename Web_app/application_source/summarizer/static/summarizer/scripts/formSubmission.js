// Get the document elements 
const $textInputField = $("#text");

const $numOfSentsRadio = $("#optionSentences");
const $numOfSentsInputField = $("#numOfSents");

const $ratioRadio = $("#optionRatio");
const $ratioInputField = $("#ratio");

const $firstSentenceRadioY = $("#firstSentenceYes");
const $firstSentenceRadioN = $("#firstSentenceNo");

const $summaryTextParagraph = $("#summaryText");

const $submitButton = $("#submitButton");


// Bind a custom function to form submission
$('#summarizerForm').submit( function() {
    SubmitForm();
    return false;
});


//-----------------------------------------------------------------
// Function called upon FORM SUBMISSION  
//-----------------------------------------------------------------
function SubmitForm(){

    // Define the request body
    var requestData = {};

    // Disable the submit button
    $submitButton.prop( 'disabled' , true );

    // Put the placehelder text inside the *summary text* paragraph and change the text color
    $summaryTextParagraph.html( 'The summary of your text will be shown here. To copy the text to the clipboard, press the <span class="fst-italic fw-bold">Copy to clipboard </span><i class="bi bi-clipboard"></i> button below.' );
    $summaryTextParagraph.css( "color",  "rgb(200, 200, 200)" );

    // Get the input text and populate the request body
    const content = $textInputField.val().trim();
    requestData["text"] = content; 

    // Check which option is checked : *number of sentences* | *sentence ratio*
    if ( $($numOfSentsRadio).is(':checked') ){
        // Get the number of sentences and populate the request body
        const numberOfSentences = parseInt( $numOfSentsInputField.val() );
        requestData["numOfSents"] = numberOfSentences;  

    }else if( $($ratioRadio).is(':checked') ){
        // Get the sentence ratio and populate the request body
        const ratio = parseFloat( $ratioInputField.val() );
        requestData["sentRatio"] = ratio;
    }

    // Check if the first sentence should be retured : *Yes* | *No*
    if( $($firstSentenceRadioY).is(':checked') ){
        // Populate the request body accordingly
        requestData["useFirstSent"] = true;

    }else if( $($firstSentenceRadioN).is(':checked') ){
        // Populate the request body accordingly
        requestData["useFirstSent"] = false;
    }

    // Send the POST request
    postRequest('http://127.0.0.1:8000/summarize', requestData)
        .then( response => {

            // If the response returned successfully
            if (response.ok){
                // Return the response body
                return response.json();
                
            }else{
                // If the response did not return successfully,
                // reject the response (calls the '.catch()' handler)
                Promise.reject(response);
            }

        })
        .then( responseBody => {
            
            // Call the 'finishSummaryFetching' function and display the summary
            finishSummaryFetching(
                {
                    "text": responseBody["content"],
                    "color": "rgb(0, 0, 0)"
                }
            );

        })
        .catch( error => {

            // Call the 'finishSummaryFetching' function and display the error message
            finishSummaryFetching(
                {
                    "text": "There was a problem while processing your text. Please try again.",
                    "color": "rgb(212, 61, 91)" 
                }
            );

        });
    
}


//-----------------------------------------------------------------
// Asynchronous POST method implementation using Fetch API
//-----------------------------------------------------------------
async function postRequest(url = '', data = {}){

    // Hide the text inside of the submit button
    const $submitButtonText = $('#submitButtonText');
    $submitButtonText.css( "display" , "none" );
    
    // Display the loading animation
    const $loadingSpinner = $('#loadingSpinner');
    $loadingSpinner.css( "display" , "inline-block" );

    // Send a POST reqest
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    });

    // Hide the loading animation
    $loadingSpinner.css( "display" , "none" );

    // Show the text inside of the submit button
    $submitButtonText.css( "display" , "inline-block" );

    // Return the response
    return response;
}


//-----------------------------------------------------------------
// Fuction that displays a summary (or error message) and resets the form
//-----------------------------------------------------------------
function finishSummaryFetching(summaryObject){

    // Display the text in the summary field and change the text color
    $summaryTextParagraph.text( summaryObject["text"] );
    $summaryTextParagraph.css( "color" , summaryObject["color"] );

    // Enable the submit button
    $submitButton.prop( "disabled" , false );

    // Reset the number fields
    $numOfSentsInputField.val( 1 );
    $ratioInputField.val( 0.2 );

    // Reset the -- Use number of sentences / sentence ratio -- checked radio button to *number of sentences*
    $numOfSentsRadio.prop( "checked" , true );
    OptionCheck();  // enables/disables certain input fields and changes container colors
    
    // Reset the -- Keep the first sentence of the text? -- radio button to *Yes*
    $firstSentenceRadioY.prop( "checked" , true );
}



