import pytest
from datetime import datetime
from pathlib import Path


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda el progreso de cada prueba en un archivo."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        log_file = Path(__file__).parent.parent / "test_progress.log"
        
        status = "PASS" if report.passed else "FAIL" if report.failed else "SKIP"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"[{timestamp}] {item.name}: {status}\n"
        
        with open(log_file, "a") as f:
            f.write(log_entry)
