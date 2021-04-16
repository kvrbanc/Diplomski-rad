//-----------------------------------------------------------------
// Utility function for COPYING TEXT TO THE CLIPBOARD 
// -- Bound on the 'click' event of the *Copy to clipboard* form button 
//-----------------------------------------------------------------
$('#copyClipboardButton').on('click', function(){

    // Define a new range
    var range = document.createRange();

    // Get the *summary text* paragraph and set it in the new range
    var $summaryParagraph = $("#summaryText");
    range.selectNode($summaryParagraph.get(0));

    // Clear all current window selection (if any)
    window.getSelection().removeAllRanges();

    // Add the new window selection
    window.getSelection().addRange(range);
    
    // Execute the "copy" command (corresponds to CTRL + C)
    document.execCommand("copy");

    // Clear all window selections
    window.getSelection().removeAllRanges(); 
})



//-----------------------------------------------------------------
// Utility function for CLEARING THE TEXT from an input field
// -- Bound on the 'click' event of the *Clear Text* form button
//-----------------------------------------------------------------
$('#clearTextButton').on('click', function(){

    // Get the textarea element and clear its value
    var $textarea = $('#text');
    $textarea.val("");

    // Call the 'ValidateText' function that performs custom textarea
    // value validation (located in the 'formValidation.js')
    ValidateText();
})