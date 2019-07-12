class BatchValidationError(Exception):
    tab = "    "

    def __init__(self, message, errors):
        count = 0
        lines = [message]
        for error in errors:
            if isinstance(error, BatchValidationError):
                count += error.count
                for line in error.lines:
                    if not line.strip().startswith("-"):
                        line = f"- {line}"
                    lines.append(f"{self.tab}{line}")
            else:
                lines.append(f"{self.tab}- {error}")
                count += 1
        self.message = "\n".join(lines)
        self.lines = lines
        self.count = count
        super(BatchValidationError, self).__init__(
            f"failed to validate batch ({self.count} errors):\n{self.message}"
        )
