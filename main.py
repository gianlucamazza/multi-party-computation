#!/usr/bin/env python3
"""
Multi-Party Computation with Threshold ECDSA Signatures

This script demonstrates a secure multi-party computation protocol using
Shamir's Secret Sharing to distribute ECDSA key shares among multiple
participants, and then collaboratively sign messages.
"""

import sys
import logging
import argparse
from typing import Optional

from mpc.signing_protocol import MPCSigningProtocol
from utils.logging_config import setup_logging

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Multi-Party Computation with Threshold ECDSA Signatures"
    )
    
    parser.add_argument(
        "-p", "--participants",
        type=int,
        default=5,
        help="Number of participants (default: 5)"
    )
    
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=3,
        help="Threshold for reconstruction (default: 3)"
    )
    
    parser.add_argument(
        "-m", "--message",
        type=str,
        default="Hello, Secure Multi-Party Computation with ECDSA!",
        help="Message to sign (default: 'Hello, Secure Multi-Party Computation with ECDSA!')"
    )
    
    parser.add_argument(
        "-l", "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level (default: INFO)"
    )
    
    parser.add_argument(
        "-f", "--log-file",
        type=str,
        help="Log to the specified file in addition to console"
    )
    
    return parser.parse_args()

def main() -> int:
    """
    Main function to demonstrate the MPC-ECDSA protocol.
    
    Returns:
        int: Exit status code (0 for success, non-zero for failure)
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    logger = logging.getLogger(__name__)
    
    try:
        # Validate arguments
        if args.threshold > args.participants:
            logger.error("Threshold cannot be greater than the number of participants")
            return 1
        
        if args.threshold < 2:
            logger.error("Threshold must be at least 2 for security")
            return 1
            
        logger.info(f"Initializing MPC protocol with {args.participants} participants "
                   f"and threshold {args.threshold}")
        
        # Initialize the protocol
        protocol = MPCSigningProtocol(args.participants, args.threshold)
        
        # Setup secure channels between participants
        logger.info("Setting up secure channels between participants")
        protocol.setup_secure_channels()
        
        # Generate and distribute key shares
        logger.info("Generating and distributing key shares")
        protocol.generate_key_shares()
        
        # Sign the message
        logger.info(f"Signing message: '{args.message}'")
        signature = protocol.sign_message(args.message)
        logger.info(f"Signature generated: {signature}")
        
        # Verify the signature
        logger.info("Verifying signature")
        is_valid = protocol.verify_signature(args.message, signature)
        
        if is_valid:
            logger.info("✅ Signature is valid")
            print("\n✅ Signature successfully generated and verified!")
            print(f"Message: '{args.message}'")
            print(f"Signature (r, s): {signature}")
        else:
            logger.error("❌ Signature verification failed")
            print("\n❌ Signature verification failed!")
            return 1
            
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())