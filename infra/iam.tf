resource "aws_iam_policy" "ecs-task-execution-policy" {
  name = "prefectEcsTaskExecutionPolicy"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "VisualEditor0",
        "Effect" : "Allow",
        "Action" : [
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:CreateSecurityGroup",
          "ec2:CreateTags",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeSubnets",
          "ec2:DescribeVpcs",
          "ec2:DeleteSecurityGroup",
          "logs:CreateLogStream",
          "ssm:DescribeParameters",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken",
          "logs:PutLogEvents",
          "ecr:BatchCheckLayerAvailability"
        ],
        "Resource" : "*"
      }
    ]
  })
}

resource "aws_iam_policy" "ecs-task-policy" {
  name = "prefectEcsTaskPolicy"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "VisualEditor0",
        "Effect" : "Allow",
        "Action" : [
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:CreateSecurityGroup",
          "ec2:CreateTags",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeSubnets",
          "ec2:DescribeVpcs",
          "ec2:DeleteSecurityGroup",
          "ecs:CreateCluster",
          "ecs:DeleteCluster",
          "ecs:DeregisterTaskDefinition",
          "ecs:DescribeClusters",
          "ecs:DescribeTaskDefinition",
          "ecs:DescribeTasks",
          "ecs:ListAccountSettings",
          "ecs:ListClusters",
          "ecs:ListTaskDefinitions",
          "ecs:RegisterTaskDefinition",
          "ecs:RunTask",
          "ecs:StopTask",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:GetLogEvents"
        ],
        "Resource" : "*"
      }
    ]
  })
}

resource "aws_iam_role" "prefect-ecs-task-execution-role" {
  name = "prefectEcsTaskExecutionRole"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ecs-tasks.amazonaws.com"
        },
        "Action" : "sts:AssumeRole",
        "Condition" : {}
      }
    ]
  })
}

resource "aws_iam_role" "prefect-ecs-task-role" {
  name = "prefectEcsTaskRole"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ec2.amazonaws.com"
        },
        "Action" : "sts:AssumeRole",
        "Condition" : {}
      },
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ssm.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      },
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ecs-tasks.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}



resource "aws_iam_role_policy_attachment" "ecs-task-execution-policy-attach" {
  role       = aws_iam_role.prefect-ecs-task-execution-role.name
  policy_arn = aws_iam_policy.ecs-task-execution-policy.arn
}

resource "aws_iam_role_policy_attachment" "ecs-task-policy-attach" {
  role       = aws_iam_role.prefect-ecs-task-role.name
  policy_arn = aws_iam_policy.ecs-task-policy.arn
}