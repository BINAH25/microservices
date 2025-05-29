output "cluster_id" {
  value = aws_ecs_cluster.micro_service_cluster.id
}

output "cluster_arn" {
  value = aws_ecs_cluster.micro_service_cluster.arn
}
