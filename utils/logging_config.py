import logging
import os
from typing import Optional

def setup_logging(log_level: Optional[str] = None, log_file: Optional[str] = None) -> None:
    """
    Configure the logging system for the application.
    
    Args:
        log_level: Optional log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                  If not provided, defaults to INFO or reads from env var LOG_LEVEL
        log_file: Optional path to log file. If provided, logs will be written to file
                 in addition to console output
    """
    # Determine log level from parameter, environment variable, or default to INFO
    if log_level is None:
        log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    
    # Convert string to logging level constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Basic configuration
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure handlers
    handlers = []
    
    # Always add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    handlers.append(console_handler)
    
    # Add file handler if log_file specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=handlers
    )
    
    # Create a logger for this module
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized at level {log_level}")