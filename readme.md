## Overview

**Project Title**: Flappy Bird AI with NEAT

**Project Description**:  
This project uses the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to train a neural network that learns to play Flappy Bird. The game is built with Pygame, and the AI agent evolves through generations to improve performance. No supervised learning or backpropagation is used — instead, NEAT evolves the network topology and weights using a genetic algorithm.

**Project Goals**:  
* Train an AI bird using neuroevolution with NEAT-Python
* Display fitness progress and evolution statistics  
* Save and replay the best-performing bird after training  
* Visualize generation stats and bird survival

---

## Instructions for Build and Use

Steps to build and/or run the software:

1. Clone or download the repository into a local folder  
2. Ensure Python 3.10+ is installed  
3. Run the training with `python main.py`  
4. After training, run `python play_best.py` to replay the best bird  
5. Optionally, run `play_manual.py` to control a bird manually for comparison

Instructions for using the software:

1. Run `main.py` to begin AI training  
2. Observe stats: score, generation, birds alive, time left  
3. The best genome will be saved as `best_bird.pkl`  
4. Run `play_best.py` to watch the best AI bird in action

---

## Development Environment

To recreate the development environment, you need the following:

* Python 3.10+
* `pygame`
* `neat-python`
* Optional: `matplotlib` for plotting fitness trends

Install dependencies with:

```{}
pip install pygame neat-python matplotlib
```

---

## Useful Resources

I found these resources helpful during development:

* [NEAT-Python Documentation](https://neat-python.readthedocs.io/en/latest/)
* [Tech With Tim NEAT Flappy Bird Tutorial](https://www.youtube.com/watch?v=czZJpMZyHDQ)
* [Pygame Documentation](https://www.pygame.org/docs/)
* [Understanding Neuroevolution](https://distill.pub/2020/understanding-evolution/)

---

## Future Work

Planned improvements and additions:

* [ ] Add visual neural network diagrams per generation  
* [ ] Display fitness graphs during/after training  
* [ ] Log data to CSV for analysis  
* [ ] Extend to other games (e.g., Dino Game, Pong)  
* [ ] Add GUI buttons for train, test, and reset