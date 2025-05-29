variable "vpc_id" {
  type    = string
  default = "vpc id"
}

variable "frontend_alb_sg_name" {
  type        = string
  description = "name of the security group load balancer"
}

variable "frontend_service_ecs_sg_name" {
  type        = string
  description = "name of the security group ec2"
}


variable "django_service_ecs_sg_name" {
  type        = string
  description = "name of the security group ec2"
}

variable "flask_service_ecs_sg_name" {
  type        = string
  description = "name of the security group ec2"
}

variable "django_db_sg_name" {
  type        = string
  description = "name of the security group database"
}


variable "flask_db_sg_name" {
  type        = string
  description = "name of the security group database"
}

variable "django_alb_sg_name" {
  type        = string
  description = "name of the security group database"
}

variable "flask_alb_sg_name" {
  type        = string
  description = "name of the security group database"
}


variable "security_group_cidr" {
  type        = string
  description = "cidr for the security group alb"
}
