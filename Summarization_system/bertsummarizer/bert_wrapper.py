from typing import List, Union, Tuple

import numpy as np
import torch
from transformers import BertModel,BertTokenizer


class BertWrapper(object):
    """The class that calculates embedding of an input text by running a forward pass on a BertModel.

    Attributes:
        __device: torch.device
            A device on which the model runs.
        __model: BertModel
            An instance of the BertModel class.
        __tokenizer: BertTokenizer
            An instance of the BertTokenizer class.

    Methods:
        get_model():
            Retrieves an instance of the BertModel class stored in a private class variable.
        get_tokenizer():
            Retrieves an instance of the BertTokenizer class stored in a private class variable.
        get_device():
            Retrieves a torch.device object stored in a private class variable.
        tokenize_text(text: str):
            Splits the text into meaningful tokens using an instance of BertTokenizer.
        convert_tokens_into_ids(text_tokens: List[str]):
            Converts the tokens into their vocabulary IDs using an instance of BertTokenizer.
        prepare_input(text: str):
            Splits the text onto meaningful tokens and converts the tokens into their vocabulary IDs.
        forward_pass(token_ids: torch.LongTensor):
            Runs a forward pass on an instance of a BertModel.
        create_sent_embedding(text: str, hidden_layers: Union[List[int], int] = -2):
            Computes the embedding of the input text by taking a mean value of the specified hidden layer(s) of the BertModel.
        create_embedding_matrix(content: List[str], hidden_layers: Union[List[int], int] = -2):
            Computes the embedding for each input sentence by running a forward pass and taking a mean value of specified hidden layer(s) of the BertModel.
    """

    def __init__(self, model_version: str = 'bert-large-uncased'):
        """Initializes an instance of the BertWrapper class.

        Args:
            model_version (str, optional): Version of the BERT model. Defaults to 'bert-large-uncased'.
        """
        # Set the device to *gpu* if it's available 
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Initialize the BERT model
        self.__model = BertModel.from_pretrained(model_version, output_hidden_states=True).to(self.__device)
        # Initialize the BERT tokenizer
        self.__tokenizer = BertTokenizer.from_pretrained(model_version)
        # Set the BERT model to 'evaluation mode'
        self.__model.eval()
    

    def get_model(self) -> BertModel:
        """Retrieves an instance of the BertModel class stored in a private class variable.

        Returns:
            BertModel : Initialized instance of a BertModel class.
        """
        return self.__model
    

    def get_tokenizer(self) -> BertTokenizer:
        """Retrieves an instance of the BertTokenizer class stored in a private class variable.

        Returns:
            BertTokenizer: Initialized instance of a BertTokenizer class.
        """
        return self.__tokenizer
    

    def get_device(self) -> torch.device:
        """Retrieves a torch.device object stored in a private class variable.

        Returns:
            torch.device: Object specifying a device on which the model runs.
        """
        return self.__device


    def tokenize_text(self, text:str ) -> List[str]:
        """Splits the text into meaningful tokens using an instance of BertTokenizer.

        Args:
            text (str): Text being tokenized.

        Returns:
            List[str]: Tokens of the input text.
        """
        return self.__tokenizer.tokenize(text)


    def convert_tokens_into_ids(self, text_tokens: List[str] ) -> List[int]:
        """Converts the tokens into their vocabulary IDs using an instance of BertTokenizer.

        Args:
            text_tokens (List[str]): Tokens which will be converted.

        Returns:
            List[int]: Vocabulary IDs of the input tokens.
        """
        return self.__tokenizer.convert_tokens_to_ids(text_tokens)
    

    def prepare_input(self, text:str ) -> torch.tensor :
        """Splits the text onto meaningful tokens and converts the tokens into their vocabulary IDs.

        Args:
            text (str): Text being tokenized and converted to vocabulary IDs

        Returns:
            torch.tensor: Vocabulary IDs of the tokenized input text.
        """
        # Split text onto meaningful tokens
        tokenized_text = self.tokenize_text(text)
        # Convert tokens into vocabulary IDs
        token_ids = self.convert_tokens_into_ids(tokenized_text)

        return torch.tensor([token_ids]).type(torch.LongTensor).to(self.__device)


    def forward_pass(self, token_ids: torch.LongTensor ) -> Tuple[torch.FloatTensor, torch.FloatTensor ,torch.FloatTensor] :
        """Runs a forward pass on an instance of a BertModel.

        Args:
            token_ids (torch.LongTensor): Vocabulary IDs of a text going through the model.

        Returns:
            Tuple[torch.FloatTensor, torch.FloatTensor ,torch.FloatTensor]: Sequence of hidden states at the output of the last layer of the BertModel, hidden state of the first token in the sequence at the output of the BertModel, hidden states of all layers of the BertModel. 
        """
        # Run a forward pass and return the values
        last_hidden_state, pooler_output, hidden_states = self.__model(token_ids)
        return last_hidden_state, pooler_output, hidden_states


    def create_sent_embedding(self, text: str, hidden_layers: Union[List[int], int] = -2) -> torch.tensor:
        """Computes the embedding of the input text by taking a mean value of the specified hidden layer(s) of the BertModel.

        Args:
            text (str): Text whose embedding will be calculated.
            hidden_layers (Union[List[int], int], optional): Hidden layer(s) from which the embedding of the input text will be calculated. Defaults to -2.

        Returns:
            torch.tensor: Embedding of the input text.
        """
        # Convert text to tokens, and tokens into vocabulary IDs
        text_token_ids = self.prepare_input(text)
        # Run a forward pass on the BertModel
        _ ,_ , hidden_states = self.forward_pass(text_token_ids)

        # Extract the values from specified hidden layers
        if type(hidden_layers) == int:
            hidden = hidden_states[hidden_layers]
        else:
            last_states = [hidden_states[i] for i in hidden_layers]
            hidden = torch.cat(tuple(last_states), dim = 1) 
        # Return the mean of extracted values
        return hidden.mean(dim=1).squeeze()
    

    def create_embedding_matrix(self, content: List[str], hidden_layers: Union[List[int], int] = -2) -> np.ndarray:
        """Computes the embedding for each input sentence by running a forward pass and taking a mean value of specified hidden layer(s) of the BertModel.

        Args:
            content (List[str]): Sentences of the input text.
            hidden_layers (Union[List[int], int], optional): Hidden layer(s) from which the embedding of each sentence will be calculated. Defaults to -2.

        Returns:
            np.ndarray: Embeddings for each sentence of the input text.
        """
        sent_embeddings = []
        # Create embedding for each input sentence
        for sentence in content:
            embedding = self.create_sent_embedding(text=sentence, hidden_layers=hidden_layers).data.cpu().numpy()
            sent_embeddings.append(np.squeeze(embedding))
        # Return the embeddings in a matrix form
        return np.asarray(sent_embeddings)
    

    def __call__(self, content: List[str], hidden_layers: Union[List[int], int] = -2) -> np.ndarray:
        """Computes the embedding for each input sentence by running a forward pass and taking a mean value of specified hidden layer(s) of the BertModel.

        Args:
            content (List[str]): Sentences of the input text.
            hidden_layers (Union[List[int], int], optional): Hidden layer(s) from which the embedding of each sentence will be calculated. Defaults to -2.

        Returns:
            np.ndarray: Embeddings for each sentence of the input text.
        """
        return self.create_embedding_matrix(content, hidden_layers)
    
