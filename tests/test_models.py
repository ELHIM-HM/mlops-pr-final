import pytest
import torch
from transformers import BertModel, BertConfig
from madewithml.models import FinetunedLLM

@pytest.fixture
def mock_batch():
    batch_size = 4
    seq_length = 10
    return {
        "ids": torch.randint(0, 1000, (batch_size, seq_length)),
        "masks": torch.ones(batch_size, seq_length, dtype=torch.int32),
        "targets": torch.randint(0, 3, (batch_size,))
    }

def test_model_forward_pass(mock_batch):
    num_classes = 3
    embedding_dim = 768
    
    # DevOps Magic: Create a tiny, untrained dummy model instantly in memory
    # This prevents Jenkins from downloading 400MB from Hugging Face during tests!
    dummy_config = BertConfig(
        vocab_size=1000, 
        hidden_size=embedding_dim, 
        num_hidden_layers=2, 
        num_attention_heads=2
    )
    llm = BertModel(dummy_config)
    
    model = FinetunedLLM(llm=llm, dropout_p=0.5, embedding_dim=embedding_dim, num_classes=num_classes)
    
    logits = model(mock_batch)
    
    assert logits.shape == (4, num_classes)
    assert isinstance(logits, torch.Tensor)