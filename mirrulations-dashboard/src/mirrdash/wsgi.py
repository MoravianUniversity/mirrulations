import docker
from redis import Redis

from mirrcore.job_queue import JobQueue
from mirrdash.dashboard_server import create_server

redis = Redis('redis')
job_queue = JobQueue(redis)
server = create_server(job_queue, docker.from_env(), redis)
app = server.app
