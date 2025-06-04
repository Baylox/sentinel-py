from scanner import scan_ports, PortScanner, PortScannerError

def basic_usage():
    """Demonstrate basic usage with the convenience function."""
    print("=== Basic Usage ===")
    try:
        # Scan common ports on localhost
        results = scan_ports("127.0.0.1", "20-25")
        
        print("Open ports:", results["open_ports"])
        print("\nDetailed results:")
        for port_info in results["scan_results"]:
            print(f"Port {port_info['port']}: {port_info['status']}", end="")
            if port_info['service']:
                print(f" ({port_info['service']})")
            else:
                print()
    
    except PortScannerError as e:
        print(f"Scan error: {e}")

def advanced_usage():
    """Demonstrate advanced usage with the PortScanner class."""
    print("\n=== Advanced Usage ===")
    try:
        # Create a scanner with custom timeout
        scanner = PortScanner(timeout=1.0)
        
        # Scan web ports on a domain
        results = scanner.scan("example.com", "80-443")
        
        print("Open ports:", results["open_ports"])
        print("\nDetailed results:")
        for port_info in results["scan_results"]:
            if port_info["status"] == "open":
                print(f"Found open port {port_info['port']} - {port_info['service']}")
    
    except PortScannerError as e:
        print(f"Scan error: {e}")

if __name__ == "__main__":
    basic_usage()
    advanced_usage() 