import torch
from torch.optim import Adam
from torch.nn import CrossEntropyLoss

from models.model import SentimentModel

from src.data.make_dataset import load_data, preprocess_data, build_vocab

from torchtext.data.utils import get_tokenizer


def train_model():
    train_data, test_data = load_data()
    tokenizer = get_tokenizer("basic_english")
    vocab = build_vocab(train_data, tokenizer)

    # train_data = preprocess_data(train_data, tokenizer, vocab)
    # test_data = preprocess_data(test_data, tokenizer, vocab)

    train_tokens, train_labels = preprocess_data(train_data, tokenizer, vocab)
    test_tokens, test_labels = preprocess_data(train_data, tokenizer, vocab)

    model = SentimentModel(
        vocab_size=len(vocab), embedding_dim=100, hidden_dim=128, output_dim=2
    )
    optimizer = Adam(model.parameters(), lr=1e-4)
    criterion = CrossEntropyLoss()

    for epoch in range(10):
        model.train()
        for inputs, labels in zip(train_tokens, train_labels):
            optimizer.zero_grad()
            outputs = model(inputs.unsqueeze(0))

            loss = criterion(outputs, labels.unsqueeze(0))
            loss.backward()
            optimizer.step()

    torch.save(model.state_dict(), "models/sentiment_model.pth")
