# Create VPC
resource "aws_vpc" "micro_service_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = var.vpc_name
  }

}

# Create public subnet
resource "aws_subnet" "micro_service_project_public_subnet" {
  count             = length(var.cidr_public_subnet)
  vpc_id            = aws_vpc.micro_service_vpc.id
  cidr_block        = element(var.cidr_public_subnet, count.index)
  availability_zone = element(var.availability_zones, count.index)
  map_public_ip_on_launch = var.map_public_ip_on_launch
  tags = {
    Name = "micro-service-proj-public-subnet-${count.index + 1}"
  }

}

# Create private subnet
resource "aws_subnet" "micro_service_project_private_subnet" {
  count             = length(var.cidr_private_subnet)
  vpc_id            = aws_vpc.micro_service_vpc.id
  cidr_block        = element(var.cidr_private_subnet, count.index)
  availability_zone = element(var.availability_zones, count.index)

  tags = {
    Name = "micro-service-proj-private-subnet-${count.index + 1}"
  }

}
# Create internet gateway
resource "aws_internet_gateway" "micro_service_project_internet_gateway" {
  vpc_id = aws_vpc.micro_service_vpc.id

  tags = {
    Name = "micro-service-proj-internet-gateway"
  }

}

# create elastic ip
resource "aws_eip" "micro_service_project_elastic_ip" {
  domain   = "vpc"
}

# create a nat gateway
resource "aws_nat_gateway" "micro_service_project_nat_gateway" {
  allocation_id = aws_eip.micro_service_project_elastic_ip.id
  subnet_id = aws_subnet.micro_service_project_public_subnet[0].id

  tags = {
    Name = "Micro-service-NAT"
  }

  depends_on = [aws_internet_gateway.micro_service_project_internet_gateway]
}


# create public route table
resource "aws_route_table" "micro_service_project_public_route_table" {
  vpc_id = aws_vpc.micro_service_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.micro_service_project_internet_gateway.id
  }

  tags = {
    Name = "micro-service-proj-public-rt"
  }
}

# Public Route Table and Public Subnet Association
resource "aws_route_table_association" "micro_service_project_public_rt_subnet_association" {
  count          = length(aws_subnet.micro_service_project_public_subnet)
  subnet_id      = aws_subnet.micro_service_project_public_subnet[count.index].id
  route_table_id = aws_route_table.micro_service_project_public_route_table.id
}

# create private route table
resource "aws_route_table" "micro_service_project_private_route_table" {
  vpc_id = aws_vpc.micro_service_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.micro_service_project_nat_gateway.id
  }

  tags = {
    Name = "micro-service-proj-private-rt"
  }
}

# Public Route Table and Public Subnet Association
resource "aws_route_table_association" "micro_service_project_private_rt_subnet_association" {
  count          = length(aws_subnet.micro_service_project_private_subnet)
  subnet_id      = aws_subnet.micro_service_project_private_subnet[count.index].id
  route_table_id = aws_route_table.micro_service_project_private_route_table.id
}