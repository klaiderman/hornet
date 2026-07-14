from typing import Annotated

from fastapi import Path

from hornet.constants import MAX_INT_ID

ResourceId = Annotated[int, Path(le=MAX_INT_ID)]
