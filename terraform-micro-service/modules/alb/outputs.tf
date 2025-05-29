output "alb_arn" {
  value = aws_lb.micro_service_alb.arn
}

output "alb_dns_name" {
  value = aws_lb.micro_service_alb.dns_name
}

output "target_group_arn" {
  value = aws_lb_target_group.micro_service_tg.arn
}

output "alb_zone_id" {
  value = aws_lb.micro_service_alb.zone_id
}