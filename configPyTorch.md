Documentação gerada por IA
# Guia de Configuração: Acelerando o EasyOCR com GPU NVIDIA (CUDA)

Este documento detalha o processo completo para configurar um ambiente de desenvolvimento Python para utilizar uma GPU NVIDIA (especificamente uma `GeForce GTX 1650`) para acelerar tarefas do `EasyOCR`, resolvendo o aviso "Neither CUDA nor MPS are available".

-----

## 1\. Objetivo

O objetivo principal era habilitar o suporte a GPU (via CUDA) para a biblioteca `EasyOCR` em um sistema com uma placa de vídeo NVIDIA `GeForce GTX 1650`, a fim de obter uma melhoria significativa na velocidade de processamento.

-----

## 2\. Diagnóstico do Problema Inicial

Ao executar o `EasyOCR`, o seguinte aviso era exibido, indicando que a biblioteca estava recorrendo ao uso da CPU por não encontrar uma instalação compatível do CUDA:

> ```
> Neither CUDA nor MPS are available - defaulting to CPU. Note: This module is much faster with a GPU.
> C:\...\UserWarning: 'pin_memory' argument is set as true but no accelerator is found...
> ```

Isso confirmou a necessidade de instalar e configurar o ecossistema NVIDIA CUDA no sistema.

-----

## 3\. Passo a Passo da Configuração

O processo foi dividido em quatro etapas principais para garantir que todos os componentes fossem compatíveis entre si.

### \#\#\# Passo 1: Atualização do Driver da NVIDIA

A primeira etapa foi garantir que o driver da placa de vídeo estivesse atualizado e otimizado para tarefas de desenvolvimento.

  - **Ação:** Acessar o aplicativo da NVIDIA.
  - **Escolha:** Entre as opções "Game Ready Driver" e "Studio Driver", foi selecionado o **Studio Driver**.
  - **Motivo:** O **Studio Driver** é otimizado para estabilidade e performance em aplicações criativas e de computação, incluindo o CUDA, sendo a escolha ideal para cargas de trabalho de Machine Learning.

### \#\#\# Passo 2: Instalação do NVIDIA CUDA Toolkit

O CUDA Toolkit é a base que permite a comunicação entre o software e a GPU. A escolha da versão correta foi crucial.

  - **Versões do PyTorch:** `torch==2.7.1`, `torchvision==0.22.1`.
  - **Análise:** Verificou-se no site oficial do PyTorch que esta versão era compatível com `CUDA 11.8` e `CUDA 12.x`.
  - **Ação:** Foi decidido instalar o **CUDA Toolkit 11.8** por ser uma versão extremamente estável e com amplo suporte.
  - **Instalação:** O download foi feito do [arquivo do CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive) e a instalação foi realizada usando a opção **"Expressa"**.

### \#\#\# Passo 3: Instalação da Biblioteca cuDNN

A `cuDNN` é uma biblioteca que otimiza operações de redes neurais profundas na GPU.

  - **Ação:** Fazer o download da versão da **cuDNN compatível com o CUDA 11.8** no [site da NVIDIA cuDNN](https://developer.nvidia.com/rdp/cudnn-archive).
  - **Instalação:** Os arquivos das pastas `bin`, `include` e `lib` do arquivo ZIP da `cuDNN` foram descompactados e copiados para as pastas correspondentes dentro do diretório de instalação do CUDA Toolkit (ex: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`).

### \#\#\# Passo 4: Reinstalação do PyTorch com Suporte a CUDA

A versão do `PyTorch` instalada via `pip` padrão não inclui suporte a CUDA. Foi necessário substituí-la.

  - **Ação 1: Desinstalar a versão existente:**
    ```bash
    pip uninstall torch torchvision torchaudio
    ```
  - **Ação 2: Instalar a versão correta para CUDA 11.8:** O comando específico, obtido no site do PyTorch, foi executado para baixar os pacotes compilados com suporte a CUDA.
    ```bash
    pip install torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1 --index-url https://download.pytorch.org/whl/cu118
    ```

-----

## 4\. Verificação Final

Para confirmar que todo o processo foi bem-sucedido, um script Python foi executado.

  - **Código de Verificação:**
    ```python
    import torch

    if torch.cuda.is_available():
        print("Sucesso! O PyTorch está configurado com CUDA.")
        print(f"Dispositivo GPU disponível: {torch.cuda.get_device_name(0)}")
    else:
        print("Algo deu errado. O PyTorch não conseguiu encontrar a GPU com CUDA.")
    ```
  - **Resultado Obtido:**
    ```
    Sucesso! O PyTorch está configurado com CUDA.
    Dispositivo GPU disponível: NVIDIA GeForce GTX 1650
    ```

-----

## 5\. Conclusão

A configuração foi concluída com sucesso. O ambiente Python agora está corretamente configurado para utilizar a GPU NVIDIA, eliminando os avisos iniciais e permitindo que o `EasyOCR` opere com performance acelerada.