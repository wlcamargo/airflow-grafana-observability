from airflow.providers.docker.operators.docker import DockerOperator

def create_docker_task(task_id, image, command):
    return DockerOperator(
        task_id=task_id,
        image=image, 
        container_name=task_id, 
        api_version="auto",
        auto_remove=True,
        command=command,
        docker_url="tcp://docker-proxy:2375",
        network_mode="airflow_default",
        mount_tmp_dir=False,
    )
