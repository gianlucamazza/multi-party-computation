from mpc.signing_protocol import MPCSigningProtocol
from utils.logging_config import setup_logging

def main():
    setup_logging()
    num_participants = 5
    threshold = 3

    protocol = MPCSigningProtocol(num_participants, threshold)
    protocol.setup_secure_channels()
    protocol.generate_key_shares()

    message = "Hello, Enhanced Multi-Party Computation with ECDSA!"
    signature = protocol.sign_message(message)
    is_valid = protocol.verify_signature(message, signature)

    if is_valid:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")

if __name__ == "__main__":
    main()