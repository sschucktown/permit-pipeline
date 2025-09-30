import subprocess

def test_pipeline_runs():
    result = subprocess.run(
        ["python", "-m", "permit_pipeline.main"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Canonical Permit Record" in result.stdout
s
