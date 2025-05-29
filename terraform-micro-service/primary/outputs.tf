output "vpc_id" {
  value = module.vpc.micro_service_project_vpc

}

output "ecr_urls" {
  value = {
    for name, mod in module.ecr_repos : name => mod.repository_url
  }
}

output "alb_dns_name" {
  value = module.frontend_alb.alb_dns_name
}

output "private_subnets_db" {
  value = slice(module.vpc.micro_service_project_private_subnets, 2, 4)
}

output "private_subnets_app" {
  value = slice(module.vpc.micro_service_project_private_subnets, 0, 2)
}