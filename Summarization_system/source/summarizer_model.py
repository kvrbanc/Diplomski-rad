from typing import List, Optional, Tuple, Union

import numpy as np
from transformers import *

from spacy.lang.en import English

from sentence_separator import SentenceSeparator
from kmeans_wrapper import KMeansWrapper
from bert_wrapper import BertWrapper


class SummarizerModel(object):
    """The class that performs text summarization.

    Attributes:
        __bert_model: BertWrapper
            An initialized instance of the BertWrapper class.
        __sentence_separator: SentenceSeparator
            An initialized instance of the SentenceSeparator class.
        __hidden_layers: Union[List[int], int]
            Hidden layer(s) from which the sentence representation will be taken.
        __random_state: int
            A fixed random seed.
    
    Methods:
        get_bert_model():
            Retrieves an instance of the BertWrapper class stored in a private class variable.
        get_sentence_separator():
            Retrieves an instance of the SentenceSeparator class stored in a private class variable.
        get_hidden_layers():
            Retrieves a hidden layers value stored in a private class variable.
        get_random_state():
            Retrieves a fixed random seed stored in a private class variable.
        separate_sentences(content: str ,min_length: int = 40, max_length: int = 600):
            Splits the input text into sentences.
        retrieve_sent_embeddings(content_sents: List[str]):
            Calculates the embeddings of input sentences.
        cluster_sent_embeddings(sent_embeddings: np.ndarray, sent_ratio: float = 0.2, num_sentences: int = None):
            Clusters the input embeddings using a specified number of clusters (number of clusters is determined by ratio/number of sentences that need to be returned).
        cluster_sentences(self, content_sents: List[str], sent_ratio: float = 0.2, num_sentences: int = None ,use_first_sent: bool = True):
            Calculates the embeddings of input sentences and clusters them using a specified number of clusters (number of clusters is determined by ratio/number of sentences that need to be returned).
        summarize(content: str, sent_ratio: float = 0.2, num_sentences: int = None, min_length: int = 40, max_length: int = 600, use_first_sent: bool = True):
            Splits the input text into sentences, calculates the sentence embeddings and clusters them using a specified number of clusters (number of clusters is determined by ratio/number of sentences that need to be returned). In other words, it calculates the summary of the input text.

    """

    def __init__(self, bert_version: str = 'bert-large-uncased', hidden_layers: Union[List[int], int] = -2, sent_sep_language=English, random_state: int = 12345):
        """Initializes an instance of the SummarizerModel class.

        Args:
            bert_version (str, optional): Version of the BERT model. Defaults to 'bert-large-uncased'.
            hidden_layers (Union[List[int], int], optional): Hidden layer(s) from which the sentence representation will be taken. Defaults to -2.
            sent_sep_language (spacy.lang.[lang].[Language], optional): Language used to separate text into sentences. Defaults to spacy.lang.en.English.
            random_state (int, optional): A fixed random seed (used for replication of results). Defaults to 12345.
        """
        # Set the random seed
        np.random.seed(random_state)
        # Initialize the BertWrapper and SentenceSeparator classes
        self.__bert_model = BertWrapper(model_version=bert_version)
        self.__sentence_separator = SentenceSeparator(language=sent_sep_language)
        # Save the remaining argument values
        self.__hidden_layers = hidden_layers
        self.__random_state = random_state
    

    def get_bert_model(self) -> BertWrapper:
        """Retrieves an instance of the BertWrapper class stored in a private class variable.

        Returns:
            BertWrapper: An initialized instance of the BertWrapper class.
        """
        return self.__bert_model
    

    def get_sentence_separator(self) -> SentenceSeparator:
        """Retrieves an instance of the SentenceSeparator class stored in a private class variable.

        Returns:
            SentenceSeparator: An initialized instance of the SentenceSeparator class.
        """
        return self.__sentence_separator
    

    def get_hidden_layers(self) -> Union[List[int], int]:
        """Retrieves a hidden layers stored in a private class variable.

        Returns:
            Union[List[int], int]:  Hidden layers from which the sentence representation will be taken (specified upon class initialization).
        """
        return self.__hidden_layers
    

    def get_random_state(self) -> int:
        """Retrieves a fixed random seed stored in a private class variable.

        Returns:
            int: A fixed random seed (specified upon class initialization). 
        """
        return self.__random_state
    

    def separate_sentences(self, content: str ,min_length: int = 40, max_length: int = 600) -> List[str]:
        """Splits the input text into sentences.

        Args:
            content (str): Input text that will be split into sentences.
            min_length (int, optional): Minimum character length of returned sentences. Defaults to 40.
            max_length (int, optional): Maximum character length of returned sentences. Defaults to 600.

        Returns:
            List[str]: Sentences of a text whose length is in the acceptable range.
        """
        return self.__sentence_separator(content=content, min_length=min_length, max_length=max_length)


    def retrieve_sent_embeddings(self, content_sents: List[str]) -> np.ndarray:
        """Calculates the embeddings of input sentences.

        Args:
            content_sents (List[str]): Input sentences whose embeddings will be calculted.

        Returns:
            np.ndarray: Embeddings of input sentences.
        """
        return self.__bert_model(content = content_sents, hidden_layers=self.__hidden_layers)


    def cluster_sent_embeddings(self, sent_embeddings: np.ndarray, sent_ratio: float = 0.2, num_sentences: int = None) -> List[int]:
        """Clusters the input embeddings using a specified number of clusters (number of clusters is determined by ratio/number of sentences that need to be returned).

        Args:
            sent_embeddings (np.ndarray): Embeddings that will be clustered.
            sent_ratio (float, optional): Ratio of the number of embeddings that need to be returned. Defaults to 0.2.
            num_sentences (int, optional): Absolute number of embeddings that need to be returned. Defaults to None.

        Returns:
            List[int]: List indices of embeddings who are closest to cluster centroids.
        """
        return KMeansWrapper(sent_embeddings, sent_ratio=sent_ratio, num_sentences=num_sentences , random_state=self.__random_state).cluster_embeddings()


    def cluster_sentences(self, content_sents: List[str], sent_ratio: float = 0.2, num_sentences: int = None ,use_first_sent: bool = True) -> Tuple[List[str], np.ndarray]:
        """Calculates the embeddings of input sentences and clusters them using a specified number of clusters (number of clusters is determined by ratio/number of sentences that need to be returned).

        Args:
            content_sents (List[str]): Input sentences whose embeddings will be calculted and clustered.
            sent_ratio (float, optional): Ratio of the number of sentences that need to be returned. Defaults to 0.2
            num_sentences (int, optional): Absolute number of sentences that need to be returned. Defaults to None.
            use_first_sent (bool, optional): Whether the first sentence of the input should be included in the output. Defaults to True.

        Returns:
            Tuple[List[str], np.ndarray]: List of sentences along with their embeddings.
        """
        # Calculate the embeddings of input sentences 
        all_sent_embeddings = self.retrieve_sent_embeddings(content_sents = content_sents)
        # Cluster the sentence embeddings using a specified number of clusters
        closest_sent_indexes = self.cluster_sent_embeddings(all_sent_embeddings, sent_ratio=sent_ratio, num_sentences=num_sentences)

        # Include the index of the first sentence if *useFirstSent* is set to true 
        if use_first_sent:
            if not closest_sent_indexes:
                closest_sent_indexes.append(0)
            elif closest_sent_indexes[0] != 0:
                closest_sent_indexes.insert(0 , 0)
        
        # Extract the sentences whose indices were closest to cluster centroids
        sentences = [content_sents[index] for index in closest_sent_indexes]
        # Extract the sentence embeddings whose indices were closest to cluster centroids
        embedded_sentences = np.asarray([all_sent_embeddings[index] for index in closest_sent_indexes])

        return sentences, embedded_sentences
    

    def summarize(self, content: str, sent_ratio: float = 0.2, num_sentences: int = None, min_length: int = 40, max_length: int = 600, use_first_sent: bool = True) -> str:
        """Splits the input text into sentences, calculates the sentence embeddings and clusters them using a specified number of clusters (number of clusters is determined by ratio/number of sentences that need to be returned). In other words, it calculates the summary of the input text.

        Args:
            content (str): Input text that will be summarized.
            sent_ratio (float, optional): Ratio of the number of input text sentences that need to be returned. Defaults to 0.2
            num_sentences (int, optional): Absolute number of input text sentences that need to be returned. Defaults to None.
            min_length (int, optional): Minimum character length of summary sentences. Defaults to 40.
            max_length (int, optional): Maximum character length of summary sentences. Defaults to 600.
            use_first_sent (bool, optional): Whether the first sentence of the input text should be included in the summary. Defaults to True.

        Returns:
            str: A summary of the input text containing sentences whose embeddings are closest to cluster centroids.
        """
        # Separate the text into sentences
        sentence_list = self.separate_sentences(content=content, min_length=min_length, max_length=max_length)

        # Calculate the sentence embeddings and cluster them (if there are any sentences)
        if sentence_list:
            sentence_list, _ = self.cluster_sentences(content_sents=sentence_list, sent_ratio=sent_ratio, num_sentences=num_sentences, use_first_sent=use_first_sent)
        
        # Return the sentences that make up the summary as a string
        return ' '.join(sentence_list)
    

    def __call__(self, content: str, sent_ratio: float = 0.2, num_sentences: int = None, min_length: int = 40, max_length: int = 600, use_first_sent: bool = True) -> str:
        """Splits the input text into sentences, calculates the sentence embeddings and clusters them using a specified number of clusters (number of clusters is determined by ratio/number). In other words, it calculates the summary of the input text.

        Args:
            content (str): Input text that will be summarized.
            sent_ratio (float, optional): Ratio of the number of input text sentences that need to be returned. Defaults to 0.2
            num_sentences (int, optional): Absolute number of input text sentences that need to be returned. Defaults to None.
            min_length (int, optional): Minimum character length of summary sentences. Defaults to 40.
            max_length (int, optional): Maximum character length of summary sentences. Defaults to 600.
            use_first_sent (bool, optional): Whether the first sentence of the input text should be included in the summary. Defaults to True.

        Returns:
            str: A summary of the input text containing sentences whose embeddings are closest to cluster centroids.
        """
        return self.summarize(content, sent_ratio, num_sentences, min_length, max_length, use_first_sent)


if __name__=="__main__":
    bodyAstrophysics2='''
    In 2016, the field of artificial intelligence was electrified by the news that AplhaGo, DeepMind's computer program, had beat Lee Sedol, the world champion of the ancient game of Go. Many had believed that this feat would require several more decades. Editorials began to wail that this was the obituary for the human race. The machines had finally crossed the Rubicon and would soon take over. There was no turning back. AlphaGo is the most advanced game-playing program ever. In chess, there are, on average, about 20 to 30 moves you can make at any time, but for Go, there are about 250 possible moves. In fact, the total number of Go game configurations exeeds the total number of atoms in the universe. It was once thought to be too difficult for a computer to count all possible moves, so when AplhaGo manages to beat Sedol, it became an instant media sensation. However, it soon became apparent that AplhaGo, no matter how sophisticated, was a one-trick pony. Winning at Go was all it could do. As Oren Etzioni, CEO of the Allen Institute for Artificial Intelligence, said, "AlphaGo can't even play chess. It can't talk about the game. My six-year-old is smarter than AlphaGo." No matter how powerful its hardware is, you cannot go up to the machine, slap it on its back, congradulate it for beating a human, and expect a coherent response. The machine is totally unaware that it made a scientific history. In fact, machine does not even know that it is a machine. We often forget that today's robots are glorified adding machines, without self-awareness, creativity, common sense, or emotions. They can excel at specific, repetitive, narrow tasks but fail at more complex ones that require general knowledge. Although the field of AI is making truly revolutionary breakthroughs, we have to put its progress in perspective. If we compare the evolution of robots to that of rocketry, we see that robotics is beyond the stage that Tsiolkovsky was in - that is, beyond the phase of speculation and theorizing. We are all well within the stage that Goddard propelled us into and are building actual prototypes that are primitive but can demonstrate that are basic principles are correct. However, we have yet to move into the next phase, the realm of von Braun, in which innovative, powerful robots would be rolling of the assembly line and building cities on distant planets. So far, robots have been spectacularly successful as remote-controlled machines. Behind the Voyager spacecraft that sailed across Jupiter and Saturn, behind the Viking landers that touched down on the surface of Mars, behind the Galileo and Cassini spacecraft that orbited the gas giants, there was a dedicated crew of humans who called the shots. Like drones, these robots simply carried out the instructions of their human handlers at Mission Control in Pasadena. All the "robots" we see in movies are either puppets, computer animations, or remote-controlled machines. But because computer power has been doubling every eighteen months for the past few decades, what can we espect in the future?
    '''

    print(SummarizerModel().summarize(bodyAstrophysics2, sent_ratio=0.4))