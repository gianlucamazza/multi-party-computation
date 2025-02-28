# Secure Multi-Party Computation (MPC) with Threshold ECDSA

## Overview

This project implements a Secure Multi-Party Computation (MPC) protocol using Python, integrated with ECDSA (Elliptic Curve Digital Signature Algorithm) for digital signatures. The implementation combines Shamir's Secret Sharing scheme with ECDSA to allow multiple parties to collaboratively sign messages without revealing their individual key shares.

> **Note**: The current implementation serves as an educational framework for understanding the principles of threshold cryptography. The signing process is currently centralized for demonstration purposes, but includes detailed comments and TODOs explaining how a proper distributed implementation would work.

## Features

- **Threshold Cryptography**: Implements an (t,n)-threshold scheme where at least t out of n participants must collaborate to sign a message
- **Shamir's Secret Sharing**: Secure polynomial-based method for distributing key shares
- **ECDSA Integration**: Industry-standard elliptic curve digital signature algorithm
- **Secure Channels**: RSA-based asymmetric encryption for key exchange and Fernet symmetric encryption for efficient communication
- **Comprehensive Logging**: Detailed logging with configurable log levels
- **Error Handling**: Robust exception handling throughout the codebase
- **Type Annotations**: Full Python type hints for better code quality and IDE support
- **Modular Architecture**: Clean separation of concerns with distinct components for different responsibilities

## Requirements

- Python 3.7+
- Dependencies:
  - ecdsa>=0.18.0
  - cryptography>=41.0.0

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/multi-party-computation.git
   ```

2. Navigate to the project directory:
   ```bash
   cd multi-party-computation
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

The project includes a command-line interface with various options:

```bash
python main.py --help
```

Output:
```
usage: main.py [-h] [-p PARTICIPANTS] [-t THRESHOLD] [-m MESSAGE]
               [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-f LOG_FILE]

Multi-Party Computation with Threshold ECDSA Signatures

options:
  -h, --help            show this help message and exit
  -p, --participants PARTICIPANTS
                        Number of participants (default: 5)
  -t, --threshold THRESHOLD
                        Threshold for reconstruction (default: 3)
  -m, --message MESSAGE
                        Message to sign (default: 'Hello, Secure Multi-Party
                        Computation with ECDSA!')
  -l, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level (default: INFO)
  -f, --log-file LOG_FILE
                        Log to the specified file in addition to console
```

#### Example Usage

```bash
# Run with default settings (5 participants, threshold 3)
python main.py

# Run with custom parameters and DEBUG level logging
python main.py --participants 7 --threshold 4 --message "Custom message" --log-level DEBUG

# Save logs to a file
python main.py --log-file mpc.log
```

### Python API

You can also use the library programmatically:

```python
from mpc.signing_protocol import MPCSigningProtocol
from utils.logging_config import setup_logging

# Set up logging with optional custom level and log file
setup_logging(log_level="INFO", log_file="mpc.log")

# Initialize the protocol with 5 participants and threshold 3
protocol = MPCSigningProtocol(num_participants=5, threshold=3)

# Set up secure communication channels between participants
protocol.setup_secure_channels()

# Generate and distribute key shares
protocol.generate_key_shares()

# Sign a message
message = "Hello, Multi-Party Computation!"
signature = protocol.sign_message(message)

# Verify the signature
is_valid = protocol.verify_signature(message, signature)
print(f"Signature valid: {is_valid}")
```

## Architecture

The project is organized into several modules:

- **mpc/**: Core multi-party computation components
  - **participant.py**: Abstract base class for MPC participants
  - **shamir_secret_sharing.py**: Implementation of Shamir's Secret Sharing scheme
  - **signing_protocol.py**: ECDSA-based threshold signing protocol
  
- **security/**: Secure communication components
  - **secure_channel.py**: Implementation of secure channels between participants
  
- **utils/**: Utility functions
  - **logging_config.py**: Centralized logging configuration

## Testing

The project includes comprehensive unit tests covering all core functionality:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test files
python -m unittest tests/test_shamir_secret_sharing.py
python -m unittest tests/test_secure_channel.py
python -m unittest tests/test_signing_protocol.py
```

## Security Considerations

This implementation provides a framework for threshold ECDSA signing, but has several important limitations:

1. **Centralized Signing**: The current signing implementation is centralized (for educational purposes) and should be replaced with a true distributed signing algorithm for production use.
2. **Key Management**: Proper key management practices should be implemented, including secure key generation, storage, and destruction.
3. **Simulated Communication**: Network communication is simulated and would need to be properly implemented for distributed deployment.
4. **Missing Authentication**: Additional security measures like participant authentication should be implemented.
5. **Side-Channel Vulnerability**: Side-channel attack protections are not implemented.
6. **Limited Error Handling**: The error handling could be more robust for production environments.
7. **Lack of Session Management**: There's no session management or timeout mechanisms.

### Recommended Production Alternatives

For production use, consider using established libraries specifically designed for secure MPC, such as:
- [TSSL-MPC](https://github.com/microsoft/TSSL-MPC) - Microsoft's MPC implementation
- [threshold-crypto](https://github.com/helium/threshold-crypto) - Threshold cryptography library
- [multiparty-ecdsa](https://github.com/ZenGo-X/multi-party-ecdsa) - Industry-standard implementation of threshold ECDSA

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
