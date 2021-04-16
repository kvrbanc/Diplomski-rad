// When the value of the textarea is changed :
// - Check the text length (needs to be > 40)
// - Check the number of words in the text (needs to be > 1)

// Sett up variables
var $textarea = $('#text');

// Bind the 'ValidateText' function on textarea *input* event
$textarea.on('input', ValidateText );


//-----------------------------------------------------------------
// Cutom textarea VALUE VALIDATION - validates text length and word count
//-----------------------------------------------------------------
function ValidateText () {

    // Get the input text
    inputText = $textarea.val().trim();

    // Check the text length (needs to be at least 41)
    if ( inputText.length == 0 ){
        // If the input text is empty, display an appropriate warning
        $textarea.get(0).setCustomValidity("Ispunite ovo polje.");
    
    }else if ( inputText.length < 41 && inputText.length > 0){
        // If the text is too short, display an appropriate warning
        $textarea.get(0).setCustomValidity("Uneseni tekst je prekratak. Mora sadržavati barem 41 znak (još je potrebno unijeti " + ( 41 - inputText.length ) + " znakova).");
    
    }else{
        // If the text is of an appropriate length, check the number of words (needs to be > 1)

        // Get the number of words
        numOfWords = inputText.split(" ").length;

        // Check the number of words
        if( numOfWords != 1 ){
            // If there is more than one word, there is no need to display a warning message
            $textarea.get(0).setCustomValidity("");

        }else{
            // If the text contains only one word, display an appropriate warning
            $textarea.get(0).setCustomValidity("Tekst mora sadržavati više od jedne riječi.");
        }

    }  

}

