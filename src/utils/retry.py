"""
Retry Utilities

This module provides retry logic with exponential backoff for handling
transient errors in database operations and API calls.
"""

import logging
import time
from functools import wraps
from typing import Any, Callable, Optional, Tuple, Type

from ..exceptions import RetryableError

logger = logging.getLogger(__name__)


def exponential_backoff(
    func: Callable = None,
    *,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None,
):
    """
    Decorator that implements exponential backoff retry logic.

    Args:
        func: The function to decorate
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        backoff_factor: Multiplier for delay after each retry
        max_delay: Maximum delay in seconds between retries
        exceptions: Tuple of exception types to catch and retry
        on_retry: Optional callback function called on each retry

    Returns:
        Decorated function with retry logic

    Example:
        @exponential_backoff(max_retries=3, initial_delay=1.0)
        def fetch_data():
            # Code that might fail transiently
            pass
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        logger.error(
                            f"Function {f.__name__} failed after {max_retries} retries: {e}"
                        )
                        raise

                    # Call retry callback if provided
                    if on_retry:
                        on_retry(e, attempt + 1)

                    logger.warning(
                        f"Function {f.__name__} failed (attempt {attempt + 1}/{max_retries}): {e}. "
                        f"Retrying in {delay:.2f} seconds..."
                    )

                    time.sleep(delay)
                    delay = min(delay * backoff_factor, max_delay)

            # This should never be reached, but just in case
            if last_exception:
                raise last_exception

        return wrapper

    # Support both @exponential_backoff and @exponential_backoff()
    if func is None:
        return decorator
    else:
        return decorator(func)


class RetryContext:
    """
    Context manager for retry operations with exponential backoff.

    Example:
        with RetryContext(max_retries=3) as retry:
            while retry.should_retry():
                try:
                    # Code that might fail
                    break
                except Exception as e:
                    retry.record_failure(e)
    """

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
        max_delay: float = 60.0,
    ):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay

        self.attempt = 0
        self.delay = initial_delay
        self.last_exception: Optional[Exception] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # If there's an unhandled exception and we've exhausted retries, re-raise it
        if exc_type and self.attempt >= self.max_retries:
            return False
        return True

    def should_retry(self) -> bool:
        """Check if another retry attempt should be made."""
        if self.attempt > 0 and self.last_exception:
            if self.attempt > self.max_retries:
                logger.error(
                    f"Max retries ({self.max_retries}) exceeded. Last error: {self.last_exception}"
                )
                raise self.last_exception

            logger.warning(
                f"Retry attempt {self.attempt}/{self.max_retries}. "
                f"Waiting {self.delay:.2f} seconds..."
            )
            time.sleep(self.delay)
            self.delay = min(self.delay * self.backoff_factor, self.max_delay)

        self.attempt += 1
        return self.attempt <= self.max_retries + 1

    def record_failure(self, exception: Exception):
        """Record a failed attempt."""
        self.last_exception = exception


def retry_on_exception(
    exceptions: Tuple[Type[Exception], ...],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> Callable:
    """
    Simplified retry decorator for specific exception types.

    Args:
        exceptions: Tuple of exception types to catch and retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        backoff_factor: Multiplier for delay after each retry

    Returns:
        Decorator function

    Example:
        @retry_on_exception((ConnectionError, TimeoutError), max_retries=5)
        def connect_to_database():
            # Code that might raise ConnectionError or TimeoutError
            pass
    """
    return exponential_backoff(
        max_retries=max_retries,
        initial_delay=initial_delay,
        backoff_factor=backoff_factor,
        exceptions=exceptions,
    )
