# VPC
resource "aws_vpc" "prefect" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "prefect"
  }
}

# SecurityGroup
resource "aws_security_group" "ecs" {
  name        = "prefect-ecs"
  description = "prefect ecs security group"
  vpc_id      = "${aws_vpc.prefect.id}"
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "prefect-ecs-sg"
  }
}

# SecurityGroup Rule
resource "aws_security_group_rule" "ecs" {
  security_group_id = "${aws_security_group.ecs.id}"
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}


# Public Subnet
resource "aws_subnet" "public" {
  vpc_id            = "${aws_vpc.prefect.id}"
  availability_zone = "ap-northeast-1a"
  cidr_block        = "10.0.1.0/24"

  tags = {
    Name = "prefect-public-subnet-1a"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  vpc_id            = "${aws_vpc.prefect.id}"
  availability_zone = "ap-northeast-1a"
  cidr_block        = "10.0.10.0/24"

  tags = {
    Name = "prefect-private-subnet-1a"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = "${aws_vpc.prefect.id}"

  tags = {
    Name = "prefect-igw"
  }
}


# Elastic IP
resource "aws_eip" "nat" {
  vpc = true

  tags = {
    Name = "prefect-nat-eip"
  }
}

# NAT Gateway
resource "aws_nat_gateway" "nat" {
  subnet_id     = "${aws_subnet.public.id}"
  allocation_id = "${aws_eip.nat.id}"

  tags = {
    Name = "prefect-nat-gw"
  }
}


# Route Table (Public)
resource "aws_route_table" "public" {
  vpc_id = "${aws_vpc.prefect.id}"

  tags = {
    Name = "prefect-public-route"
  }
}

# Route (Public)
resource "aws_route" "public" {
  destination_cidr_block = "0.0.0.0/0"
  route_table_id         = "${aws_route_table.public.id}"
  gateway_id             = "${aws_internet_gateway.main.id}"
}

# Association (Public)
resource "aws_route_table_association" "public" {
  subnet_id      = "${aws_subnet.public.id}"
  route_table_id = "${aws_route_table.public.id}"
}


# Route Table (Private)
resource "aws_route_table" "private" {
  vpc_id = "${aws_vpc.prefect.id}"

  tags = {
    Name = "prefect-private-route"
  }
}

# Route (Private)
resource "aws_route" "private" {
  destination_cidr_block = "0.0.0.0/0"
  route_table_id         = "${aws_route_table.private.id}"
  nat_gateway_id         = "${aws_nat_gateway.nat.id}"
}

# Association (Private)
resource "aws_route_table_association" "private" {
  subnet_id      = "${aws_subnet.private.id}"
  route_table_id = "${aws_route_table.private.id}"
}
