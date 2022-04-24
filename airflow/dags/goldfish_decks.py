from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sys
import os

sys.path.append("/".join(os.path.abspath(__file__).split("/")[0:4]))
from extract.scraped_websites.spiders.goldfish_decks import GoldFishSpiderDecks
from scrapy.crawler import CrawlerProcess
from utils.config_helper import configHelper


def create_dag(format: str):
    default_args = {
        "owner": "admin2",
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "reries": 2,
        "retry_delay": timedelta(minutes=2),
    }
    config_helper = configHelper()

    def extract(format: str):
        output = config_helper.get_dataset_path()
        process = CrawlerProcess(
            settings={"FEEDS": {f"{output}/{format}.json": {"format": "json"}}}
        )
        process.crawl(GoldFishSpiderDecks, format="standard")
        process.start()

    def clean(format: str):
        print(f"\n\n{format}")

    def transform(format: str):
        print(f"\n\n{format}")

    def load(format: str):
        print(f"\n\n{format}")

    dag = DAG(
        format,
        schedule_interval=timedelta(weeks=1),
        default_args=default_args,
        start_date=days_ago(2),
    )
    with dag:
        extract_task = PythonOperator(
            task_id="Extract", python_callable=extract, op_kwargs={"format": format}
        )
        clean_task = PythonOperator(
            task_id="Clean", python_callable=clean, op_kwargs={"format": format}
        )
        transform_task = PythonOperator(
            task_id="Transform", python_callable=transform, op_kwargs={"format": format}
        )
        load_task = PythonOperator(
            task_id="Load", python_callable=load, op_kwargs={"format": format}
        )
        extract_task >> clean_task >> transform_task >> load_task
    return dag


globals()["standard"] = create_dag("standard")
globals()["modern"] = create_dag("modern")
globals()["pioneer"] = create_dag("pioneer")
globals()["pauper"] = create_dag("pauper")
