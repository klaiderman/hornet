from hornet.core.patterns import CAMEL_BOUNDARY

def to_title(name: str) -> str:
    return CAMEL_BOUNDARY.sub(" ", name)
