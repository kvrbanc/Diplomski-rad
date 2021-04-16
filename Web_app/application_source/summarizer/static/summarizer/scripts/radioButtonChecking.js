// Get the document elements
const $radios = $('[name="radioOption"]');

const $numOfSentsField = $("#numOfSents");
const $ratioField = $("#ratio");

const $numOfSentsDiv = $("#sentInputDiv");
const $ratioDiv = $("#ratioInputDiv");

// Define the colors for 'enabled' and 'disabled' elements
disabledColor = "repeating-linear-gradient( 45deg, #d9d9d9, #d9d9d9 10px, #cccccc 10px, #cccccc 20px)"
enabledColor = "rgb(230, 230, 230)";


//-----------------------------------------------------------------
// Function called upon CLICKING ON the specific RADIO BUTTONS
//-----------------------------------------------------------------
function OptionCheck(){

    // Look for the 'checked' radio button and change the appearance of its parent container
    $.each( $radios, function(index, $radioButton) {

        if( $($radioButton).is(':checked')){
            if( $($radioButton).attr('id') == "optionRatio" ){
                // Enable the *sentence ratio* and disable the *number of sentences* input field
                $ratioField.prop( 'disabled', false );
                $numOfSentsField.prop( 'disabled', true );

                // Set the *number of sentences* input field to default value
                $numOfSentsField.val( 1 );

                // Change the background colors of the input fields' parent containers
                $numOfSentsDiv.css( "background", disabledColor );
                $ratioDiv.css( "background", "none" );
                $ratioDiv.css( "background", enabledColor );

            }else if( $($radioButton).attr('id') == "optionSentences"){
                // Enable the *number of sentences* and disable the *sentence ratio* input field
                $numOfSentsField.prop( 'disabled', false );
                $ratioField.prop( 'disabled', true );

                // Set the *sentence ratio* input field to default value
                $ratioField.val( 0.2 );

                // Change the background colors of the input fields' parent containers
                $ratioDiv.css( "background", disabledColor );
                $numOfSentsDiv.css( "background", "none" );
                $numOfSentsDiv.css( "background", enabledColor );
            }

        }

    });

}