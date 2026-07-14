from fastapi import FastAPI

from hornet.main import Application

def test_application_exposes_fastapi_app():
    assert isinstance(Application().app, FastAPI)

def test_stop_before_run_is_a_noop():
    Application().stop()
