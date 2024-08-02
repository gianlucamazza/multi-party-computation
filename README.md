# Secure Multi-Party Computation (MPC) Project with ECDSA

## Overview

This project implements a Secure Multi-Party Computation (MPC) protocol using Python, integrated with ECDSA (Elliptic Curve Digital Signature Algorithm) for digital signatures. The implementation combines Shamir's Secret Sharing scheme with ECDSA to allow multiple parties to collaboratively sign messages without revealing their individual key shares.

## Table of Contents

- [Secure Multi-Party Computation (MPC) Project with ECDSA](#secure-multi-party-computation-mpc-project-with-ecdsa)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [How It Works](#how-it-works)
  - [Security Considerations](#security-considerations)

## Features

- Implementation of Shamir's Secret Sharing for secure distribution of key shares
- Integration with ECDSA for digital signatures
- Support for an arbitrary number of participants
- Secure collaborative signing of messages
- Error handling and input validation
- Modular design for easy extension and modification

## Requirements

- Python 3.7+
- ecdsa library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mpc-ecdsa-project.git
   ```
2. Navigate to the project directory:
   ```
   cd mpc-ecdsa-project
   ```
3. Install the required dependencies:
   ```
   pip install ecdsa
   ```

## How It Works

The MPC-ECDSA protocol in this project operates as follows:

1. **Key Generation**: A private ECDSA key is generated and split into shares using Shamir's Secret Sharing scheme.
2. **Share Distribution**: Each participant receives a share of the private key.
3. **Signing**: When signing a message, each participant contributes to the signature using their key share.
4. **Signature Reconstruction**: The partial signatures are combined to create the final ECDSA signature.
5. **Verification**: The signature can be verified using the corresponding public key.

The use of Shamir's Secret Sharing ensures that no single participant can reconstruct the entire private key from their share alone.

## Security Considerations

While this implementation provides a basic framework for MPC-ECDSA, it is primarily intended for educational purposes. For production use, consider the following:

- Implement secure channels for share distribution
- Use cryptographically secure random number generation
- Implement threshold signatures for increased security
- Consider using a more established MPC-ECDSA library or framework
- Conduct a thorough security audit before any real-world application
