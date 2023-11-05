# Deep Learning Vocal Separator

This project hosts a neural network specifically trained to separate vocal and instrumental tracks from songs by Post Malone. The architecture is the work of github user: tsurumeso and has been trained with a dataset consisting solely of Post Malone songs, due to time constraints. It was trained for 36 epochs spanned across ~26 hours. It was developed as part of a TigerHacks hackathon project, and due to the targeted nature of its training and time constraints, it performs optimally on Post Malone tracks.

## Prerequisites

Before running this application, please refer to `requirements.txt` for a list of prerequisites.

## Installation

1. Download the zip of the vocal remover repo
2. Export it to some directory on your computer
3. Open a terminal and perform the following commands:
```bash
cd your\dir\to\vocal-remover
pip install -r requirements.txt
