import pytest

from api.petstore_client import PetstoreClient


_api_results = []


@pytest.fixture(scope="function")
def api_client() -> PetstoreClient:
    return PetstoreClient()


def pytest_runtest_logreport(report):
    if report.when == "call" and report.nodeid.startswith("tests/api/"):
        _api_results.append(report)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if not _api_results:
        return

    total = len(_api_results)
    passed = sum(1 for result in _api_results if result.passed)
    failed = sum(1 for result in _api_results if result.failed)
    skipped = sum(1 for result in _api_results if result.skipped)

    terminalreporter.write_sep("=", "RELATORIO API - estilo Postman/Newman")
    terminalreporter.write_line("+----------------+-------+")
    terminalreporter.write_line("| Metrica        | Total |")
    terminalreporter.write_line("+----------------+-------+")
    terminalreporter.write_line(f"| Executed       | {total:>5} |")
    terminalreporter.write_line(f"| Passed         | {passed:>5} |")
    terminalreporter.write_line(f"| Failed         | {failed:>5} |")
    terminalreporter.write_line(f"| Skipped        | {skipped:>5} |")
    terminalreporter.write_line("+----------------+-------+")

    if failed:
        terminalreporter.write_line("")
        terminalreporter.write_line("Failure Detail:")
        for result in _api_results:
            if result.failed:
                failure_line = str(result.longrepr).splitlines()[-1]
                terminalreporter.write_line(f"- {result.nodeid}: {failure_line}")
    else:
        terminalreporter.write_line("Failure Detail: nenhuma falha encontrada.")
