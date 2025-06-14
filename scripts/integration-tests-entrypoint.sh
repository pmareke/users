#!/bin/sh

alembic upgrade head 2>/dev/null

"$@"
