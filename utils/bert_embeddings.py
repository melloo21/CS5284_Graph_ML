import torch
from sentence_transformers import SentenceTransformer

class SentenceEmbeddingModel(torch.nn.Module):
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        """
        Initialize the SentenceEmbeddingModel with a pre-trained SBERT model.
        
        Args:
            model_name (str): The name of the pre-trained Sentence-BERT model.
        """
        super(SentenceEmbeddingModel, self).__init__()
        
        # Load the SBERT model
        self.sbert_model = SentenceTransformer(model_name)
    
    def forward(self, texts):
        """
        Forward pass to convert input texts to sentence embeddings.
        
        Args:
            texts (str or list): Input text or list of texts.
        
        Returns:
            torch.Tensor: A tensor of shape (batch_size, embedding_size) representing the sentence embeddings.
        """
        # Check if input is a single string, and convert to list for consistency
        if isinstance(texts, str):
            texts = [texts]
        
        # Convert the list of texts to sentence embeddings
        embeddings = self.sbert_model.encode(texts, convert_to_tensor=True)
        
        return embeddings