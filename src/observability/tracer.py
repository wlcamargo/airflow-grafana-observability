from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import set_tracer_provider, get_tracer


class TelemetryTracer:
    """
    Implementation of the Tracer setup using OpenTelemetry SDK.
    """

    def __init__(self):
        self.tracer_provider = None

    def setup(self, otlp_endpoint, app_name):
        """
        Sets up OpenTelemetry tracing.

        :param otlp_endpoint: Endpoint for exporting traces to OpenTelemetry.
        :param app_name: Name of the application for OpenTelemetry resource configuration.
        """
        resource = Resource(attributes={"service.name": app_name})
        self.tracer_provider = TracerProvider(resource=resource)
        set_tracer_provider(self.tracer_provider)

        span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        span_processor = BatchSpanProcessor(span_exporter)
        self.tracer_provider.add_span_processor(span_processor)

    def start_span(self, name, **kwargs):
        """
        Starts a new trace span with the given name and optional attributes.

        :param name: The name of the span.
        :param kwargs: Optional attributes to add to the span.
        """
        if self.tracer_provider is None:
            raise RuntimeError("Tracer provider not set up.")
        tracer = get_tracer(__name__)
        return tracer.start_span(name, **kwargs)


def setup_tracing(otlp_endpoint, app_name):
    resource = Resource(attributes={"service.name": app_name})
    trace_provider = TracerProvider(resource=resource)
    set_tracer_provider(trace_provider)

    span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    span_processor = BatchSpanProcessor(span_exporter)
    trace_provider.add_span_processor(span_processor)