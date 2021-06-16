from typing import List, Dict, Union

import numpy as np
from numpy import ndarray

from sklearn.cluster import KMeans



class KMeansWrapper(object):
    """The class that performs clustering and determining the embeddings closest to centroids.

    Attributes:
        __sent_embeddings:
            Embeddings of the sentences being clustered.
        __sent_ratio:
            Ratio of the number of input sentence embeddings whose indices need to be returned.
        __num_sentences:
            Absolute number of input sentence embeddings whose indices need to be returned.
        __random_state:
            A fixed random seed.
        __model:
            An instance of the KMeans class.
    
    Methods:
        get_model():
            Retrieves an instance of the KMeans class stored in a private class variable.
        get_random_state():
            Retrieves the random seed number stored in a private class variable.
        get_sent_embeddings():
            Retrieves the embeddings of sentences stored in a private class variable.
        get_sent_ratio():
            Retrieves the sentence ratio stored in a private class variable.
        get_num_sentences():
            Retrieves the number of sentences stored in a private class variable.
        fit_model():
            Fits the KMeans model stored in a private class variable using sentence embeddings specified upon class initialization.
        retrieve_centroids():
            Retrieves the centroids of the fitted KMeans object stored in a private class variable.
        find_closest_sents(cluster_centroids : np.ndarray):
            Determines the list indices of sentence embeddings who are closest to cluster centroids. Sentence embeddings are specified upon class initialization. 
        cluster_embeddings():
            Fits the KMeans model using the sentence embeddings specified upon class initialization, determines the list indices of the embeddings who fall closest to cluster centroids and returns those indices.
    """


    def __init__(self, sent_embeddings: ndarray, sent_ratio: float = 0.2, num_sentences: int = None, random_state: int = 12345):
        """Initializes an instance of the KMeansWrapper class.

        Args:
            sent_embeddings (ndarray): Embeddings of the sentences being clustered.
            sent_ratio (float, optional): Ratio of the number of input sentence embeddings whose indices need to be returned. Defaults to 0.2.
            num_sentences (int, optional): Absolute number of input sentence embeddings whose indices need to be returned. Defaults to None.
            random_state (int, optional): A fixed random seed (used for replication of results). Defaults to 12345.
        """
        # Store the provided values
        self.__sent_embeddings = sent_embeddings
        self.__sent_ratio = sent_ratio
        self.__num_sentences = num_sentences
        self.__random_state = random_state
        # Instantiate the KMeans clustering model
        self.__model = self.__instantiate_model()
    
        
    def __instantiate_model(self) -> KMeans:
        """Initializes an instance of the KMeans clustering model.

        Returns:
            KMeans: Instance of the KMeans clustering model.
        """
        # Calculate the number of clusters using *number of sentences*/*sentence ratio*
        if self.__num_sentences is not None:
            n_clusters = min(self.__num_sentences, len(self.__sent_embeddings))
        else:
            n_clusters = max(int(len(self.__sent_embeddings)* self.__sent_ratio), 1)
            
        # Initialize a KMeans object
        return KMeans(n_clusters=n_clusters , random_state = self.__random_state)
    

    def get_model(self) -> KMeans:
        """Retrieves an instance of the KMeans class stored in a private class variable.

        Returns:
            KMeans: Initialized KMeans clustering model
        """
        return self.__model
    

    def get_random_state(self) -> int:
        """Retrieves the random seed number stored in a private class variable.

        Returns:
            int: Fixed random seed.
        """
        return self.__random_state
    

    def get_sent_embeddings(self) -> np.ndarray:
        """Retrieves the embeddings of sentences stored in a private class variable.

        Returns:
            numpy.ndarray: Sentence embeddings.
        """
        return self.__sent_embeddings
    

    def get_sent_ratio(self) -> float:
        """Retrieves the sentence ratio stored in a private class variable.

        Returns:
            float: The ratio of the number of embeddings that need to be returned.
        """
        return self.__sent_ratio
    

    def get_num_sentences(self) -> Union[int, None]:
        """Retrieves the number of sentences stored in a private class variable.

        Returns:
            Union[int, none]: The absolute number of embeddings that need to be returned.
        """
        return self.__num_sentences
    
    
    def fit_model(self) -> KMeans:
        """Fits the KMeans model stored in a private class variable using sentence embeddings specified upon class initialization.

        Returns:
            KMeans: A fitted KMeans object.
        """
        # Fit the model and return it
        self.__model = self.__model.fit(self.__sent_embeddings)
        return self.__model
    

    def retrieve_centroids(self) -> np.ndarray:
        """Retrieves the centroids of the fitted KMeans object stored in a private class variable.

        Returns:
            numpy.ndarray: Coordinates of cluster centroids.
        """
        return self.__model.cluster_centers_


    def find_closest_sents(self, cluster_centroids : np.ndarray) -> Dict[int,int] : 
        """Determines the list indices of sentence embeddings who are closest to cluster centroids. Sentence embeddings are specified upon class initialization. 

        Args:
            cluster_centroids (np.ndarray): Coordinates of cluster centroids.

        Returns:
            Dict[int,int]: Dictionary whose keys are the centroid indices and values are list indices of the embeddings closest to those centroids.
        """
        # Set up variables
        min_distance = 1e10
        used_sent_indexes = []
        curr_sent_num = -1
        closest_sentences = {}

        # For every centroid
        for cent_num, centroid in enumerate(cluster_centroids):
            # For every sentence embedding, determine the distance to centroid
            for sent_num, sent_features in enumerate(self.__sent_embeddings):
                distance = np.linalg.norm(sent_features - centroid)
                # Remember the index of the sentence embedding with the minimum distance 
                if distance < min_distance and sent_num not in used_sent_indexes :
                    curr_sent_num = sent_num
                    min_distance = distance
            # Store the index of the sentence embedding with minimum distance and reset the variables
            used_sent_indexes.append(curr_sent_num)
            closest_sentences[cent_num] = curr_sent_num
            min_distance = 1e10
            curr_sent_num = -1
        
        return closest_sentences


    
    def cluster_embeddings(self) -> List[int] :
        """Fits the KMeans model using the sentence embeddings specified upon class initialization, determines the list indices of the embeddings who fall closest to cluster centroids and returns those indices.

        Returns:
            List[int]: Sorted list indices of the sentence embeddings who fall closest to cluster centroids.
        """
        # If the *number of sentence* is 0, return empty list
        if self.__num_sentences is not None:
            if self.__num_sentences == 0:
                return []

        # Fit the model and retrieve cluster centroids
        clustering_model = self.fit_model()
        centroids = self.retrieve_centroids()

        # Find the list indices of the sentence embeddings who fall closest to cluster centroids
        closest_sentences = self.find_closest_sents(centroids)

        # Sort the list indices and return them
        sorted_indices = sorted(closest_sentences.values())
        return sorted_indices
    

    def __call__(self) -> List[int] :
        """Fits the KMeans model using the sentence embeddings specified upon class initialization, determines the list indices of the embeddings who fall closest to cluster centroids and returns those indices.

        Returns:
            List[int]: Sorted list indices of the sentence embeddings who fall closest to cluster centroids.
        """
        return self.cluster_embeddings()



