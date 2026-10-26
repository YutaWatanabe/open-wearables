from app.services.providers.base_strategy import BaseProviderStrategy, ProviderCapabilities, ProviderCoverage
from app.services.providers.statebell.coverage import TIMESERIES


class StatebellStrategy(BaseProviderStrategy):
    """First-party manual records sent through the shared SDK import pipeline."""

    @property
    def name(self) -> str:
        return "statebell"

    @property
    def display_name(self) -> str:
        return "StateBell"

    @property
    def api_base_url(self) -> str:
        return ""

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(client_sdk=True)

    @property
    def coverage(self) -> ProviderCoverage:
        return ProviderCoverage(timeseries=TIMESERIES)
