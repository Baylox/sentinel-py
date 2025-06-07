import logging
from typing import Dict, Any
from scanner.logging_advanced import log_with_context
from scanner.utils.exporter import export_to_json

def display_results(results: Dict[str, Any]) -> None:
    """
    Display scan results to the user with logging.
    
    Args:
        results: Dictionary containing scan results
    """
    logger = logging.getLogger("sentinelpy")
    log_with_context(logger, logging.DEBUG, "Rendering results to stdout", context="DISPLAY")
    
    # Format and display results
    print("\nScan Results:")
    print("-" * 50)
    
    for port, status in results.items():
        print(f"Port {port}: {status}")
    
    print("-" * 50)
    log_with_context(logger, logging.INFO, "Results displayed successfully", context="DISPLAY")

def handle_output(results: Dict[str, Any], args: Any) -> None:
    """
    Handle output/export of scan results with logging.
    
    Args:
        results: Dictionary containing scan results
        args: Command line arguments
    """
    logger = logging.getLogger("sentinelpy")
    
    if args.json:
        log_with_context(logger, logging.INFO, f"Exporting results to {args.json}", context="EXPORT")
        try:
            import json
            with open(args.json, 'w') as f:
                json.dump(results, f, indent=2)
            log_with_context(logger, logging.INFO, "Results exported successfully", context="EXPORT")
        except Exception as e:
            log_with_context(logger, logging.ERROR, f"Export failed: {str(e)}", context="EXPORT")
            raise
    
    if args.print_json:
        log_with_context(logger, logging.DEBUG, "Printing results as JSON", context="EXPORT")
        import json
        print(json.dumps(results, indent=2))
        log_with_context(logger, logging.INFO, "Results printed as JSON", context="EXPORT")

    else:
        # Default: export with an auto-generated name or default behavior
        export_to_json(results) 