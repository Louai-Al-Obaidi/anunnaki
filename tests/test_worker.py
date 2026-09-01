"""Focused behavior tests for the sequential conversion worker."""

from pathlib import Path

from doc2markdown_desktop.conversion import ConversionError
from doc2markdown_desktop.validation import OutputPolicy
from doc2markdown_desktop.worker import ConversionRequest, ConversionWorker


def _events(worker: ConversionWorker) -> list[tuple[int, str, str]]:
    events: list[tuple[int, str, str]] = []
    worker.item_finished.connect(
        lambda index, status, detail: events.append((index, status, detail))
    )
    return events


def test_worker_creates_output_and_reports_success(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "report.txt"
    source.write_text("source", encoding="utf-8")
    destination = tmp_path / "report.md"

    def fake_convert(input_path: Path, output_path: Path) -> None:
        assert input_path == source
        assert output_path == destination
        output_path.write_text("# converted", encoding="utf-8")

    monkeypatch.setattr("doc2markdown_desktop.worker.convert_file", fake_convert)
    worker = ConversionWorker([ConversionRequest(source)], OutputPolicy.AUTO_RENAME)
    events = _events(worker)

    worker.run()

    assert destination.read_text(encoding="utf-8") == "# converted"
    assert events == [(0, "Complete", str(destination))]


def test_worker_skips_existing_output_when_requested(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "report.txt"
    source.write_text("source", encoding="utf-8")
    (tmp_path / "report.md").write_text("existing", encoding="utf-8")
    monkeypatch.setattr(
        "doc2markdown_desktop.worker.convert_file",
        lambda *_: (_ for _ in ()).throw(AssertionError("conversion should not run")),
    )
    worker = ConversionWorker([ConversionRequest(source)], OutputPolicy.SKIP)
    events = _events(worker)

    worker.run()

    assert events == [(0, "Skipped", "Output already exists")]


def test_worker_preserves_a_failed_conversion_and_continues(tmp_path: Path, monkeypatch) -> None:
    failed = tmp_path / "broken.txt"
    succeeded = tmp_path / "ok.txt"
    failed.write_text("broken", encoding="utf-8")
    succeeded.write_text("ok", encoding="utf-8")

    def fake_convert(input_path: Path, output_path: Path) -> None:
        if input_path == failed:
            raise ConversionError("converter failed")
        output_path.write_text("ok", encoding="utf-8")

    monkeypatch.setattr("doc2markdown_desktop.worker.convert_file", fake_convert)
    worker = ConversionWorker(
        [ConversionRequest(failed), ConversionRequest(succeeded)], OutputPolicy.AUTO_RENAME
    )
    events = _events(worker)

    worker.run()

    assert events[0] == (0, "Failed", "converter failed")
    assert events[1] == (1, "Complete", str(tmp_path / "ok.md"))
    assert (tmp_path / "ok.md").read_text(encoding="utf-8") == "ok"


def test_worker_cancellation_marks_pending_items(tmp_path: Path, monkeypatch) -> None:
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("first", encoding="utf-8")
    second.write_text("second", encoding="utf-8")
    worker = ConversionWorker(
        [ConversionRequest(first), ConversionRequest(second)], OutputPolicy.AUTO_RENAME
    )
    events = _events(worker)

    def fake_convert(_: Path, output_path: Path) -> None:
        output_path.write_text("first", encoding="utf-8")
        worker.cancel()

    monkeypatch.setattr("doc2markdown_desktop.worker.convert_file", fake_convert)
    worker.run()

    assert events[0] == (0, "Complete", str(tmp_path / "first.md"))
    assert events[1] == (1, "Cancelled", "Conversion cancelled")
