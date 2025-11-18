"""
Registry and factory for casting methods.

Manages all available casting methods and provides lookup by element.
"""

from typing import Optional, List
from .base import CastingMethod, Element
from .metal import MetalMethod
from .wood import WoodMethod
from .fire import FireMethod
from .earth import EarthMethod
from .air import AirMethod


class CastingMethodRegistry:
    """
    Registry and factory for casting methods.

    Manages all available casting methods and provides
    lookup by element.
    """

    def __init__(self):
        self._methods: dict[Element, CastingMethod] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register the five element methods"""
        self.register(MetalMethod())
        self.register(WoodMethod())
        self.register(FireMethod())
        self.register(EarthMethod())  # Without seed initially
        self.register(AirMethod())

    def register(self, method: CastingMethod) -> None:
        """
        Register a new casting method.

        Args:
            method: CastingMethod instance to register
        """
        self._methods[method.element] = method

    def get(self, element: Element) -> Optional[CastingMethod]:
        """
        Get casting method by element.

        Args:
            element: Element enum value

        Returns:
            CastingMethod instance or None if not found
        """
        return self._methods.get(element)

    def list_methods(self) -> List[CastingMethod]:
        """
        List all registered methods.

        Returns:
            list: All registered CastingMethod instances
        """
        return list(self._methods.values())

    def get_available_methods(self) -> List[CastingMethod]:
        """
        List all currently available methods.

        Checks is_available() for each method and returns only
        those that are currently usable.

        Returns:
            list: CastingMethod instances that are currently available
        """
        available = []
        for method in self._methods.values():
            is_avail, _ = method.is_available()
            if is_avail:
                available.append(method)
        return available

    def get_method_info(self, element: Element) -> dict:
        """
        Get detailed information about a casting method.

        Args:
            element: Element enum value

        Returns:
            dict: Method information including availability
        """
        method = self.get(element)
        if method is None:
            return {
                'element': element.value,
                'available': False,
                'error': 'Method not found'
            }

        is_avail, error = method.is_available()

        return {
            'element': element.value,
            'name': method.name,
            'description': method.description,
            'requires_network': method.requires_network,
            'available': is_avail,
            'error': error
        }

    def list_all_info(self) -> List[dict]:
        """
        Get information about all registered methods.

        Returns:
            list: Information dicts for all methods
        """
        return [
            self.get_method_info(method.element)
            for method in self._methods.values()
        ]


# Singleton instance
_registry = CastingMethodRegistry()


def get_registry() -> CastingMethodRegistry:
    """Get the global casting method registry"""
    return _registry
