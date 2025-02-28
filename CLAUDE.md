# Multi-Party Computation Codebase Guide

## Commands
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate   # On Unix/macOS
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the main application
python main.py

# Run with custom parameters
python main.py --participants 7 --threshold 4 --message "Custom message" --log-level DEBUG

# Run tests
python -m unittest discover tests

# Lint with flake8
flake8 .

# Type checking with mypy
mypy .

# Format code with black
black .
```

## Code Style Guidelines
- **Imports**: Standard library first, third-party second, local imports last
- **Formatting**: 4-space indentation, 100 character line limit
- **Types**: Use type annotations for all function parameters and return values
- **Naming**:
  - Classes: CamelCase (ex: MPCParticipant)
  - Functions/methods: snake_case (ex: generate_shares)
  - Variables: snake_case (ex: private_key)
  - Private methods/attributes: prefix with underscore (ex: _mod_inverse)
- **Error Handling**: Use descriptive exception messages, log errors using the logging module
- **Documentation**: Include docstrings for all modules, classes, and functions (Google format)
- **Logging**: Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- **Structure**: Maintain the package organization (mpc, security, utils)
- **Tests**: Write unit tests for all functionality
- **Comments**: TODO comments should explain what needs to be implemented