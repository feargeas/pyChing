"""
Casting methods for I Ching oracle.

This module implements five distinct casting methods, each corresponding
to one of the Five Elements (Wu Xing) of Chinese philosophy. Each method
uses a different source of randomness while maintaining the traditional
I Ching probabilities.
"""

from .base import Element, CastingMethod
from .metal import MetalMethod
from .wood import WoodMethod
from .fire import FireMethod
from .earth import EarthMethod
from .air import AirMethod
from .registry import CastingMethodRegistry, get_registry

__all__ = [
    'Element',
    'CastingMethod',
    'MetalMethod',
    'WoodMethod',
    'FireMethod',
    'EarthMethod',
    'AirMethod',
    'CastingMethodRegistry',
    'get_registry',
]
