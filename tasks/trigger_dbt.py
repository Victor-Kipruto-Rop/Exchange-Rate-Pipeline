import subprocess

def run_dbt():
    result = subprocess.run(
        ["dbt", "run", "--project-dir", "/opt/airflow/dbt_project"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"dbt run failed:\n{result.stderr}")
    print(result.stdout)
