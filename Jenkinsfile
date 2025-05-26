def COLOR_MAP = [
    'SUCCESS': 'good', 
    'FAILURE': 'danger',
]

pipeline {
    agent any

    environment {
        ECR_REGISTRY = credentials('ecr-registry')
        ECR_REPOSITORY = credentials('admin-service')
        AWS_REGION = credentials('aws-region')
        QUEUE_REPO = credentials('admin-service-queue')
        CLUSTER = credentials('cluster')

        registryCredential = "ecr:${AWS_REGION}:awscreds"
        djangoRegistry = "${ECR_REGISTRY}/${ECR_REPOSITORY}"
        queueRegistry = "${ECR_REGISTRY}/${QUEUE_REPO}"
        registryUrl = "https://${ECR_REGISTRY}"
        cluster = "${CLUSTER}"
        adminservice = 'django'
        queueservice = 'django-queue'
    }

   
    stages {

        stage('Fetch code') {
            steps {
                git branch: 'main', url: 'https://github.com/BINAH25/microservices.git'
            }
        }

// admin service Jenkins Pipeline
        stage('SonarQube analysis') {
            when { changeset "admin/*"}
            environment {
                scannerHome = tool 'sonar'
            }
            steps {
                dir('admin') {
                    withSonarQubeEnv('sonar') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            when { changeset "admin/*"}
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build App Images') {
            when { changeset "admin/*"}
            steps {
                script {
                    djangoImage = docker.build("${djangoRegistry}:$BUILD_NUMBER", "./admin/")
                    queueImage = docker.build("${queueRegistry}:$BUILD_NUMBER", "-f ./admin/Dockerfile.queue ./admin/")
                }
            }
        }

        stage('Scan Django Image with Trivy') {
            when { changeset "admin/*"}
            steps {
                script {
                    sh """
                        trivy image --format table --severity HIGH,CRITICAL ${djangoRegistry}:$BUILD_NUMBER || exit 1
                    """
                }
            }
        }

        stage('Scan Queue Image with Trivy') {
            when { changeset "admin/*"}
            steps {
                script {
                    sh """
                        trivy image --format table --severity HIGH,CRITICAL ${queueRegistry}:$BUILD_NUMBER || exit 1
                    """
                }
            }
        }

        stage('Upload Images to ECR') {
            when { changeset "admin/*"}
            steps {
                script {
                    docker.withRegistry(registryUrl, registryCredential) {
                        djangoImage.push("$BUILD_NUMBER")
                        djangoImage.push('latest')

                        queueImage.push("$BUILD_NUMBER")
                        queueImage.push('latest')
                    }
                }
            }
        }


        stage('Deploy Admin Image to ecs') {
            when { changeset "admin/*"}
            steps {
                withAWS(credentials: 'awscreds', region: "${AWS_REGION}") {
                    sh """
                        aws ecs update-service \
                        --cluster ${cluster} \
                        --service ${adminservice} \
                        --force-new-deployment
                    """
                }
            }
        }

        stage('Deploy Queue Image to ecs') {
            when { changeset "admin/*"}
            steps {
                withAWS(credentials: 'awscreds', region: "${AWS_REGION}") {
                    sh """
                        aws ecs update-service \
                        --cluster ${cluster} \
                        --service ${queueservice} \
                        --force-new-deployment
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Sending detailed Slack notification'
            script {
                // Getting Git information
                def gitCommitShort = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                def gitAuthor = sh(script: "git show -s --pretty=%an", returnStdout: true).trim()
                def gitCommitMsg = sh(script: "git log -1 --pretty=%B", returnStdout: true).trim()
                def buildDuration = currentBuild.durationString.replace(' and counting', '')
                def buildStatus = currentBuild.currentResult                
                //Slack message
                def slackMessage = """
                :jenkins: *${buildStatus}*: Job `${env.JOB_NAME}` #${env.BUILD_NUMBER}
                *Image Tag:* ${BUILD_NUMBER}
                *Git Commit:* ${gitCommitShort} | ${gitCommitMsg}
                *Author:* ${gitAuthor}
                *Duration:* ${buildDuration}
                *More Info:* <${env.BUILD_URL}|View Build> | <${env.BUILD_URL}console|Console Output>
                """
                
                slackSend(
                    channel: '#micro-service-pipelines',
                    color: COLOR_MAP[buildStatus],
                    message: slackMessage
                )
            }
        }
        
    }
}