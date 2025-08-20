Documentação gerada por IA
# Configuração de Ambiente de Deep Learning com CUDA

## 1\. Objetivo

Configurar um ambiente de desenvolvimento em um notebook Acer Nitro 5 com uma GPU **NVIDIA GeForce GTX 1650** para projetos de Visão Computacional (easyOCR, YOLO). O objetivo é utilizar a aceleração de hardware (GPU) através do ecossistema NVIDIA CUDA.

**Data de Conclusão:** 19 de agosto de 2025
**Hardware:** Acer Nitro 5
**GPU:** NVIDIA GeForce GTX 1650
**Sistema Operacional:** Windows

-----

## 2\. Verificação de Compatibilidade e Drivers

O primeiro passo foi garantir que o hardware era compatível e que os drivers estavam corretos.

### 2.1. Compatibilidade da GPU

  - A **GeForce GTX 1650** foi confirmada como compatível com CUDA.
  - Sua **Capacidade de Computação (Compute Capability)** é de **7.5**, o que é suportado pelas versões mais recentes das bibliotecas de Deep Learning.

### 2.2. Atualização do Driver Gráfico

  - O driver da NVIDIA foi atualizado para a versão mais recente através do aplicativo oficial **NVIDIA App**.
  - **Ação:** Realizada a instalação limpa do driver para evitar conflitos.
  - **Verificação:** A versão do driver foi confirmada como superior à mínima exigida pelos Toolkits. A verificação do driver e da versão máxima do CUDA suportada foi feita pelo comando:
    ```bash
    nvidia-smi
    ```

-----

## 3\. Instalação de Dependências

O CUDA Toolkit para Windows requer um compilador C++, que é fornecido pelo Microsoft Visual Studio.

### 3.1. Instalação do Visual Studio

  - **Software:** Microsoft Visual Studio Community 2022 (versão gratuita).
  - **Componente Essencial:** Durante a instalação, foi selecionada a carga de trabalho **"Desenvolvimento para desktop com C++"**. Este passo é crucial, pois instala o compilador MSVC necessário para o CUDA Toolkit.

-----

## 4\. Instalação do CUDA Toolkit

Este é o núcleo do ambiente de aceleração da NVIDIA.

### 4.1. Download e Instalação

  - **Versão Escolhida:** **CUDA Toolkit 11.8**, selecionada por ser uma versão estável e amplamente compatível com a versão desejada do PyTorch.
  - **Processo de Instalação:**
    1.  O instalador foi executado como **Administrador**.
    2.  Foi selecionada a opção de instalação **Personalizada (Avançada)**.
    3.  Durante a seleção de componentes, o item **"Display Driver"** foi desmarcado para não sobrescrever o driver mais novo já instalado.
    4.  A instalação foi concluída com sucesso após resolver um conflito inicial com o NVIDIA App.

### 4.2. Verificação da Instalação do Toolkit

  - A confirmação foi feita via linha de comando, que é o método definitivo.
  - **Comando:**
    ```bash
    nvcc --version
    ```
  - **Resultado Esperado:** O terminal retornou a versão `11.8`, confirmando que o compilador e as ferramentas do CUDA foram instaladas e adicionadas ao PATH do sistema.

-----

## 5\. Instalação da Biblioteca cuDNN

A cuDNN (CUDA Deep Neural Network library) é uma biblioteca que acelera primitivas de redes neurais profundas.

### 5.1. Download e Instalação Manual

  - **Versão:** Foi baixada uma versão do cuDNN compatível com o CUDA 11.8 do site NVIDIA Developer.
  - **Procedimento:** Como o cuDNN não possui um instalador, os arquivos foram copiados manualmente:
    1.  O conteúdo do arquivo `.zip` do cuDNN foi extraído para uma pasta temporária.
    2.  **Todos os arquivos** das pastas `bin`, `include` e `lib` do cuDNN foram copiados para as pastas de mesmo nome dentro do diretório de instalação do CUDA Toolkit.
    <!-- end list -->
      - **Diretório de Destino:** `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\`

-----

## 6\. Configuração do Ambiente Python e Verificação Final

O passo final é instalar a biblioteca de Deep Learning (PyTorch) e confirmar que ela consegue acessar a GPU.

### 6.1. Instalação do PyTorch com Suporte a CUDA

  - A instalação foi feita utilizando o `pip`, especificando a versão do CUDA para garantir que os binários corretos fossem baixados.
  - **Comando:**
    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

### 6.2. Teste de Verificação Final

  - Um script Python foi executado para garantir que todo o ecossistema (Driver -\> CUDA -\> cuDNN -\> PyTorch) estivesse se comunicando corretamente.
  - **Código de Teste:**
    ```python
    import torch

    # Verifica se o CUDA está disponível para o PyTorch
    cuda_disponivel = torch.cuda.is_available()
    print(f"CUDA disponível? {cuda_disponivel}")

    if cuda_disponivel:
        # Mostra o nome da GPU
        print(f"Nome da GPU: {torch.cuda.get_device_name(0)}")
    ```
  - **Resultado:** O script retornou `True` e o nome "NVIDIA GeForce GTX 1650", confirmando que o ambiente está **100% funcional e pronto** para o desenvolvimento.