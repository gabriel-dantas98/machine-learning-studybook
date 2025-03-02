import sys
import structlog

if sys.stderr.isatty():
    # Pretty printing when we run in a terminal session.
    # Automatically prints pretty tracebacks when "rich" is installed
    processors = [
        structlog.dev.ConsoleRenderer(),
    ]
else:
    # Print JSON when we run, e.g., in a Docker container.
    # Also print structured tracebacks.
    processors = [
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ]

structlog.configure(processors)

log = structlog.get_logger()
