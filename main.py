def validate_code(s: str) -> bool:
    if len(s) != 5:
        return False
    
    if s[0] not in ('+', '-'):
        return False
    
    if not s[1:].isdigit():
        return False
    
    return True


def main():
    pass

main()