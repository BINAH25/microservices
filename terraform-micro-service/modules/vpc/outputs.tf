output "micro_service_project_vpc" {
  value = aws_vpc.micro_service_vpc.id

}

output "micro_service_project_public_subnets" {
  value = aws_subnet.micro_service_project_public_subnet.*.id
}

output "micro_service_project_private_subnets" {
  value = aws_subnet.micro_service_project_private_subnet.*.id
}