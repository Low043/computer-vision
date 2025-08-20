import torch

# A função torch.cuda.is_available() é o teste definitivo.
# Ela retornará True se o PyTorch conseguir se comunicar com a GPU via CUDA.
if torch.cuda.is_available():
    print("Sucesso! O PyTorch está configurado com CUDA.")
    print(f"Dispositivo GPU disponível: {torch.cuda.get_device_name(0)}")
else:
    print("Algo deu errado. O PyTorch não conseguiu encontrar a GPU com CUDA.")