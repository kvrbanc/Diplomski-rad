from typing import List

# spacy==2.1.0
from spacy.lang.en import English
from spacy.tokens import Doc

class SentenceSeparator(object):
    """The class that separates text onto its sentences.

    Attributes:
        __nlp: spacy.lang.[lang].[Language]
            A initialized language processing pipeline.
    
    Methods:
        get_language_pipeline():
            Retrieves a spacy language processing pipeline stored in a private variable.
        generate_doc(content: str):
            Processes the input text using a language pipeline specified upon class initialization.
        retrieve_doc_sents(doc: Doc , min_length: int = 40 , max_length: int = 600):
            Retrieves sentences of an appropriate length from a spacy Doc object.
        process_content(content: str, min_length: int = 40 , max_length: int = 600):
            Processes the text using a language pipeline and retrieves the text sentences of an appropriate length.
    """


    def __init__(self, language=English):
        """Initializes an instance of the SentenceSeparator class.

        Args:
            language (spacy.lang.[lang].[Language], optional): Language used to separate text into sentences. Defaults to spacy.lang.en.English.
        """
        # Store the language object
        self.__nlp = language()
        # Add a *sentencizer* to the language pipeline
        self.__nlp.add_pipe(self.__nlp.create_pipe('sentencizer'))


    def get_language_pipeline(self):
        """Retrieves a spacy language processing pipeline stored in a private variable.

        Returns:
            spacy.lang.[lang].[Language] : An initialized spacy language processing pipeline.
        """
        return self.__nlp


    def generate_doc(self, content: str ) -> Doc:
        """Processes the input text using a language pipeline specified upon class initialization.

        Args:
            content (str): Text that will be processed.

        Returns:
            Doc: Object containing linguistic annotations of the input text.
        """
        return self.__nlp(content)


    def retrieve_doc_sents(self, doc: Doc , min_length: int = 40 , max_length: int = 600) -> List[str]:
        """Retrieves sentences of an appropriate length from a spacy Doc object.

        Args:
            doc (Doc): Object containing linguistic annotations of a text.
            min_length (int, optional): Minimum character length of returned sentences. Defaults to 40.
            max_length (int, optional): Maximum character length of returned sentences. Defaults to 600.

        Returns:
            List[str]: Sentences of a text whose Doc object was given as the input.
        """
        content_sentences=[]
        # Retrieve sentences of an appropriate length from a Doc
        for sentence in doc.sents:
            if max_length > len(sentence.text.strip()) > min_length :
                content_sentences.append(sentence.text.strip())

        return content_sentences


    def process_content(self, content: str, min_length: int = 40 , max_length: int = 600) -> List[str]:
        """Processes the text using a language pipeline and retrieves the text sentences of an appropriate length.

        Args:
            content (str): Text whose sentences will be retrieved.
            min_length (int, optional): Minimum character length of returned sentences. Defaults to 40.
            max_length (int, optional): Maximum character length of returned sentences. Defaults to 600.

        Returns:
            List[str]: Sentences of the input text.
        """
        # Process text using a language pipeline
        doc = self.generate_doc(content=content)

        # Retrieve sentences from a Doc object
        return self.retrieve_doc_sents( doc=doc , min_length=min_length , max_length=max_length)
    

    def __call__(self, content: str, min_length: int = 40 , max_length: int = 600) -> List[str]:
        """Processes the text using a language pipeline and retrieves the text sentences of an appropriate length.

        Args:
            content (str): Text whose sentences will be retrieved.
            min_length (int, optional): Minimum character length of returned sentences. Defaults to 40.
            max_length (int, optional): Maximum character length of returned sentences. Defaults to 600.

        Returns:
            List[str]: Sentences of the input text.
        """
        return self.process_content(content, min_length, max_length)



    
    



