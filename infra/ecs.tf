resource "aws_ecs_cluster" "prefect-ecs" {
  name = "prefect-ecs"
}

resource "aws_cloudwatch_log_group" "prefect-log-group" {
  name              = "prefect-flow"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "prod-prefect-agent" {
  family                   = "prod-prefect-agent"
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  requires_compatibilities = ["FARGATE"]
  container_definitions    = templatefile("./prefect-ecs-agent-task.json", { prefect_api_key = "${var.prefect_api_key}", log_group = "${aws_cloudwatch_log_group.prefect-log-group.name}" })
  task_role_arn            = "${aws_iam_role.prefect-ecs-task-execution-role.arn}"
  execution_role_arn       = "${aws_iam_role.prefect-ecs-task-role.arn}"
}

resource "aws_ecs_service" "prod-prefect-agent" {
  name                               = "prefect-ecs-agent"
  cluster                            = "${aws_ecs_cluster.prefect-ecs.name}"
  task_definition                    = aws_ecs_task_definition.prod-prefect-agent.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 200
  launch_type                        = "FARGATE"
  network_configuration {
    security_groups = [
      "${aws_security_group.ecs.id}"
    ]
    subnets = [
      "${aws_subnet.private.id}"
    ]
  }
}
