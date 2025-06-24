from scanner.utils.logging_tools import clear_logs, show_logs

def handle_utility_operations(args):
    """
    Handle utility operations such as log display or cleanup.

    Args:
        args: Parsed CLI arguments

    Returns:
        bool: True if an operation was performed, False otherwise
    """
    if getattr(args, "clear_logs", False):
        clear_logs()
        print("Logs successfully deleted.")
        return True

    if getattr(args, "show_logs", False):
        logs = show_logs(getattr(args, "logfile", None))
        print("Log contents:\n", logs)
        return True

    return False

