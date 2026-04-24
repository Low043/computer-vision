import torch


def detect_accelerator():
    # Em builds ROCm, PyTorch continua expondo o backend como "cuda",
    # então diferenciamos por torch.version.hip.
    if torch.cuda.is_available():
        backend = "ROCm (HIP)" if torch.version.hip else "CUDA"
        return backend, "cuda", torch.cuda.get_device_name(0)

    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "MPS", "mps", "Apple GPU"

    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return "XPU", "xpu", torch.xpu.get_device_name(0)

    return None, "cpu", "CPU"


def main():
    backend, device, device_name = detect_accelerator()

    print(f"PyTorch: {torch.__version__}")
    print(f"Build CUDA: {torch.version.cuda or 'não'}")
    print(f"Build ROCm/HIP: {torch.version.hip or 'não'}")

    if backend is None:
        print("Nenhum acelerador de GPU detectado. Execução em CPU.")
        return

    print(f"Sucesso! Backend detectado: {backend}")
    print(f"Dispositivo disponível: {device_name} ({device})")


if __name__ == "__main__":
    main()
