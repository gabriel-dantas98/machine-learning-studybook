import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel


# Carrega o tokenizer e o modelo BERT em português
MODEL_NAME = "neuralmind/bert-base-portuguese-cased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
bert_model = AutoModel.from_pretrained(MODEL_NAME)
bert_model.eval()  # Modo de inferência


def get_text_embedding(text: str) -> np.ndarray:
    """
    Gera o embedding para o texto utilizando o BERT em português.
    Utiliza o vetor do token [CLS] como representação semântica.
    """
    print("Generating text embedding...")
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, padding=True, max_length=128
    )
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # Extrai o embedding do token [CLS] (posição 0)
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
    return cls_embedding.astype(np.float32)


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calcula similaridade de cosseno entre dois vetores."""
    if vec1 is None or vec2 is None:
        return 0.0
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))
