from jason.database import postgres_engine, scoped_session
from .service import LoggingService
from .database import session_factory


def build(testing=False, management_api=False) -> LoggingService:
    config = service.ServiceConfig.load()
    db_engine = postgres_engine(config=config, testing=testing)
    database.session_factory.configure(bind=db_engine)
    if management_api:
        management_api_db_handler = scoped_session(session_factory)
        management_api = service.LoggingManagementApi(
            config=config, db_handler=management_api_db_handler
        )
    logging_service_db_handler = scoped_session(session_factory)
    logging_service = LoggingService(
        config=config,
        db_handler=logging_service_db_handler,
        sidekicks=(management_api,) if management_api else (),
    )
    return logging_service
