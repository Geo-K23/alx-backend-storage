#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""
import requests
import redis
from functools import wraps
from typing import Callable


# Initialize Redis client
redis_client = redis.Redis()


def cache_with_expiration(func: Callable) -> Callable:
    """
    Decorator to cache the result of a function with an expiration time.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Wrapper function that adds caching functionality to the original
        function.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        """
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"

        # Check if the result is cached
        cached_result = redis_client.get(cache_key)
        if cached_result:
            # Increment the access count
            redis_client.incr(count_key)
            return cached_result.decode('utf-8')

        # If not cached, call the original function
        result = func(url)

        # Cache the result with a 10-second expiration time
        redis_client.setex(cache_key, 10, result)

        # Increment the access count
        redis_client.incr(count_key)

        return result

    return wrapper


@cache_with_expiration
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL, track access count,
    and cache with expiration.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
