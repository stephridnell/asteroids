# Asteroids Game

A classic Asteroids game implementation using Python and Pygame. Navigate through space, shoot asteroids, and try to survive as long as possible!

## Features

- Smooth player movement and rotation
- Asteroid spawning system with different sizes
- Collision detection between player, shots, and asteroids
- Asteroid splitting mechanics when shot
- Classic arcade-style gameplay

## Controls

- **W/↑**: Move forward
- **S/↓**: Move backward
- **A/←**: Rotate left
- **D/→**: Rotate right
- **SPACE**: Shoot
- **ESC**: Quit game

## Requirements

- Python 3.x
- Pygame 2.6.1

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/asteroids.git
cd asteroids
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Game

# Run without debug mode (default)

python main.py

# Run with debug mode enabled

python main.py --debug

## Game Rules

- Control your spaceship and avoid colliding with asteroids
- Shoot asteroids to split them into smaller pieces
- Game ends if you collide with an asteroid
- Asteroids spawn from the edges of the screen
- Smaller asteroids move faster than larger ones

## Project Structure

- `main.py`: Main game loop and initialization
- `player.py`: Player ship implementation
- `asteroid.py`: Asteroid behavior and splitting mechanics
- `asteroidfield.py`: Asteroid spawning system
- `shot.py`: Projectile implementation
- `circleshape.py`: Base class for circular game objects
- `constants.py`: Game configuration and constants

## TODO

- Implement multiple lives and respawning
- Add an explosion effect for the asteroids
- Add acceleration to the player movement
- Create different weapon types
- Add a shield power-up
- Add a speed power-up
- Add bombs that can be dropped

## License

This project is open source and available under the MIT License.
