from typing import Annotated

from fastapi import Path

ResourceId = Annotated[int, Path(le=2_147_483_647)]
