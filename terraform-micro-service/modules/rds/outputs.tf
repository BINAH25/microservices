output "db_hostname" {
  value = aws_db_instance.postgres.address
}

output "db_instance_arn" {
  value = aws_db_instance.postgres.arn
}
