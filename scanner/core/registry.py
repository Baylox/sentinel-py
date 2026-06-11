from typing import Dict, Type, List, Optional

class ScannerRegistry:
    """
    Registry for dynamic discovery and instantiation of scanners.
    """
    _scanners: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: str):
        """
        Decorator to register a scanner class under a specific name.
        """
        def decorator(scanner_class):
            cls._scanners[name] = scanner_class
            return scanner_class
        return decorator

    @classmethod
    def get_scanner(cls, name: str) -> Optional[Type]:
        """
        Retrieve a scanner class by name.
        """
        return cls._scanners.get(name)

    @classmethod
    def get_available_modules(cls) -> List[str]:
        """
        Get a list of all registered scanner names.
        """
        return list(cls._scanners.keys())
