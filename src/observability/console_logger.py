import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


class ConsoleLogger:
    """
    A simple console logger for logging messages to the console and OpenTelemetry.
    """

    def __init__(self, otlp_endpoint=None, app_name="app-send-log"):
        """
        Initializes the ConsoleLogger with a StreamHandler and optional OpenTelemetry handler.

        :param otlp_endpoint: Optional OTLP endpoint for exporting logs to OpenTelemetry.
        :param app_name: Name of the application for OpenTelemetry resource configuration.
        """
        self.logger = logging.getLogger("src.logging.console_logger")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
            
            if otlp_endpoint:
                self._setup_opentelemetry_handler(otlp_endpoint, app_name)

    def _setup_opentelemetry_handler(self, endpoint, app_name):
        """
        Sets up the OpenTelemetry LoggingHandler.

        :param endpoint: The OTLP endpoint to export logs to.
        :param app_name: The name of the application for OpenTelemetry resource configuration.
        """
        resource = Resource({SERVICE_NAME: app_name})
        provider = LoggerProvider(resource=resource)

        otlp_exporter = OTLPLogExporter(endpoint=endpoint, insecure=True)

        processor = BatchLogRecordProcessor(
            otlp_exporter,
            max_queue_size=2048, 
            max_export_batch_size=512, 
        )
        provider.add_log_record_processor(processor)
        set_logger_provider(provider)

        otlp_handler = LoggingHandler(level=logging.DEBUG, logger_provider=provider)
        self.logger.addHandler(otlp_handler)

    def info(self, message):
        """
        Logs a message with level INFO.

        :param message: The message to log.
        """
        self.logger.info(message)

    def error(self, message):
        """
        Logs a message with level ERROR.

        :param message: The message to log.
        """
        self.logger.error(message)

    def debug(self, message):
        """
        Logs a message with level DEBUG.

        :param message: The message to log.
        """
        self.logger.debug(message)