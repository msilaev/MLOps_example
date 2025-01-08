import torch
from src.models.model import SentimentModel


def predict(text, model_path, tokenizer, vocab):
    model = SentimentModel(
        vocab_size=len(vocab), embedding_dim=100, hidden_dim=128, output_dim=2
    )

    model.load_state_dict(torch.load(model_path))
    model.eval()

    inputs = torch.tensor(vocab(tokenizer(text)))
    outputs = model(inputs.unsqueeze(0))

    return torch.argmax(outputs).item()
