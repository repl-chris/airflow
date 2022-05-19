#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from datetime import timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

# This dag should not get loaded directly, it should only
# be loaded via the symlink

args = {
    'owner': 'airflow',
}

dag = DAG(
    dag_id='symlink_test_dag_1',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
)

EmptyOperator(
    task_id='empty',
    dag=dag,
)

if __name__ == "__main__":
    dag.cli()
