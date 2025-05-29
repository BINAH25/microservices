variable "region" {
  type        = string
  description = "AWS region"
}

variable "vpc_cidr" {
  type = string
}

variable "cidr_public_subnet" {
  type = list(string)
}

variable "cidr_private_subnet" {
  type = list(string)
}

variable "availability_zones" {
  type = list(string)
}

variable "vpc_name" {
  type = string
}

variable "map_public_ip_on_launch" {
  type    = bool
  default = true
}

variable "cluster_name" {
  type = string
}



variable "frontend_alb_sg_name" {
  type = string

}

variable "frontend_service_ecs_sg_name" {
  type = string

}


variable "django_alb_sg_name" {
  type = string

}

variable "django_service_ecs_sg_name" {
  type = string

}

variable "django_db_sg_name" {
  type = string

}


variable "flask_alb_sg_name" {
  type = string

}

variable "flask_service_ecs_sg_name" {
  type = string

}

variable "flask_db_sg_name" {
  type = string

}

variable "security_group_cidr" {
  type = string
}

variable "db_instance_class" {
  type = string
}


variable "storage_type" {
  type = string
}

variable "domain_name" {
  type = string
}

variable "alternative_names" {
  type = list(string)
}

# variable "instance_type" {
#   type    = string
#   default = "t2.micro"
# }

# variable "key_name" {
#   type = string
# }

# variable "instance_name" {
#   type = string
# }

# variable "associate_public_ip_address" {
#   type    = bool
#   default = true
# }


variable "ecr_repositories" {
  type = list(string)
  default = [
    "admin-service",
    "admin-service-queue",
    "user-service",
    "user-service-queue",
    "frontend-service"
  ]
}

variable "django_secret" {
  type = string
}

variable "flask_secret" {
  type = string
}