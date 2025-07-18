# -*- coding: utf-8 -*-
from services.Actions import CliSession
import services.Actions

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('mysql+pymysql://root:password@localhost:3306/bank')
with Session(engine) as session:
    cli_session = CliSession(session)
    cli_session.start()
    session.commit()




