from app.schemas.enums import SeriesType

# The first StateBell manual entry is a single drink, stored in millilitres.
TIMESERIES: frozenset[SeriesType] = frozenset({SeriesType.hydration})
