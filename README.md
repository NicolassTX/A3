# Space Shooter

Jogo 2D de nave espacial desenvolvido em Python com Pygame. Destrua asteroides, desvie dos perigos e colete bonus para tentar alcancar a maior pontuacao.

## Objetivo

Sobreviver pelo maior tempo possivel. Cada asteroide destruido concede 10 pontos. A cada 100 pontos, o nivel aumenta e os asteroides ficam mais rapidos e aparecem com maior frequencia. A partida termina quando as tres vidas acabam. Colidir com um asteroide ou deixar que ele passe pela parte inferior da tela custa uma vida. Depois de perder uma vida, a nave fica protegida por 1 segundo.

## Recursos do jogo

- Tres tamanhos de asteroides, com velocidades diferentes.
- Dificuldade progressiva de ate 10 niveis: a cada 100 pontos, os asteroides ficam mais rapidos e aparecem com maior frequencia.
- Asteroides aparecem em uma faixa mais central da tela.
- Perder um asteroide que chega ao fim da tela tambem custa uma vida.
- Bonus de tiro rapido: colete o cristal verde para disparar mais rapidamente por 6 segundos.
- Pausa durante a partida.
- Nave representada por uma imagem PNG incluida no projeto.

## Controles

- **Seta para a esquerda** ou **A**: mover para a esquerda.
- **Seta para a direita** ou **D**: mover para a direita.
- **Espaco**: disparar (segure para continuar atirando).
- **P**: pausar ou continuar a partida.
- **Enter**: iniciar ou jogar novamente; tambem continua quando pausado.
- **M**: voltar ao menu na tela de Game Over.
- **Esc**: sair do jogo.

## Tecnologias utilizadas

- Python 3
- Pygame

## Estrutura do projeto

```text
SpaceShooter/
├── main.py
├── requirements.txt
├── README.md
└── assets/
    └── nave.png
```

## Instalacao

1. Tenha o Python 3 instalado.
2. Abra o terminal na pasta `SpaceShooter`.
3. (Opcional, recomendado) Crie e ative um ambiente virtual:

   **Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **Linux/macOS:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Instale a dependencia:

   ```bash
   pip install -r requirements.txt
   ```

## Como executar

Na pasta do projeto, execute:

**Windows:**
```bash
python main.py
```

**Linux/macOS:**
```bash
python3 main.py
```
