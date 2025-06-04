from scanner.utils.exporter import clean_exports, list_exports

def handle_utility_operations(args):
    """
    Handle utility operations like listing or cleaning exports.
    
    Args:
        args: Parsed CLI arguments
        
    Returns:
        bool: True if a utility operation was handled
    """
    if args.list_exports:
        list_exports()
        return True
        
    if args.clean_exports:
        clean_exports()
        return True
        
    return False 