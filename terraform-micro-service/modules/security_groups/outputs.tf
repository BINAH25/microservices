output "frontend_alb_sg_name" {
  value = aws_security_group.frontend_alb_sg.id

}

output "frontend_service_sg_name" {
  value = aws_security_group.frontend_service_sg.id

}
output "django_db_sg_name" {
  value = aws_security_group.django_db_sg.id
}

output "flask_db_sg_name" {
  value = aws_security_group.flask_db_sg.id
}
output "djando_alb_sg_name" {
  value = aws_security_group.django_alb_sg.id

}

output "flask_alb_sg_name" {
  value = aws_security_group.flask_alb_sg.id

}

output "django_service_sg_name" {
  value = aws_security_group.django_service_sg.id

}

output "flask_service_sg_name" {
  value = aws_security_group.flask_service_sg.id

}