from pprint import pprint
from scanner.utils.exporter import export_to_json

def display_results(results: dict):
    """
    Display the results of the port scan in a readable format.

    Args:
        results (dict): Dictionary containing scan results.
    """
    if results["open_ports"]:
        print("\nOpen ports found:")
        for port in results["open_ports"]:
            port_info = next(r for r in results["scan_results"] if r["port"] == port)
            service = f" ({port_info['service']})" if port_info['service'] else ""
            print(f"  Port {port}{service}")
    else:
        print("\nNo open ports found.")

    print(f"\nScan complete: {len(results['scan_results'])} ports scanned.")

def handle_output(results: dict, args):
    """
    Handle how the scan results are output based on CLI options.

    Args:
        results (dict): Scan result data.
        args (argparse.Namespace): Parsed CLI arguments.
    """
    if args.json:
        # Export to a specified JSON file
        export_to_json(results, args.json)
    elif args.print_json:
        # Print results as formatted JSON to stdout
        pprint(results)
    else:
        # Default: export with an auto-generated name or default behavior
        export_to_json(results) 