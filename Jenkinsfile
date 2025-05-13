def COLOR_MAP = [
    'SUCCESS': 'good', 
    'FAILURE': 'danger',
]
pipeline {
    agent any

    environment {
        ECR_REGISTRY = credentials('ecr-registry')
        ECR_REPOSITORY = credentials('ecr-repository')
        AWS_REGION = credentials('aws-region')
        
        registryCredential = "ecr:${AWS_REGION}:awscreds"
        appRegistry = "${ECR_REGISTRY}/${ECR_REPOSITORY}"
        frontendRegistry = "https://${ECR_REGISTRY}"
        cluster = 'frontend-cluster'
        service = 'frontend-cluster-service'
    }

   
    stages {

        stage('Fetch code') {
            steps {
                git branch: 'main', url: 'https://github.com/BINAH25/microservices-react.git'
            }
        }


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

        stage('Buid App Image') {
            when { changeset "admin/*"}
            steps {
                script {
                    dockerImage = docker.build( appRegistry + ":$BUILD_NUMBER", "./admin/")
                }
            }
        }


        stage('Scan Image with Trivy') {
            when { changeset "admin/*"}
            steps {
                script {
                    sh """
                        trivy image --format table --severity HIGH,CRITICAL ${appRegistry}:$BUILD_NUMBER || exit 1
                    """
                }
            }
        }


        // stage('Upload Image to ECR') {
        //     steps {
        //         script {
        //             docker.withRegistry( frontendRegistry, registryCredential ){
        //                 dockerImage.push("$BUILD_NUMBER")
        //                 dockerImage.push('latest')
        //             }
        //         }
        //     }
        // }

        // stage('Deploy to ecs') {
        //     steps {
        //         withAWS(credentials: 'awscreds', region: 'eu-west-1') {
        //             sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'
        //         }
        //     }
        // }
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
                def imageTag = "${appRegistry}:${BUILD_NUMBER}"
                
                //Slack message
                def slackMessage = """
                :jenkins: *${buildStatus}*: Job `${env.JOB_NAME}` #${env.BUILD_NUMBER}
                *Repository:* ${ECR_REPOSITORY}
                *Image Tag:* ${BUILD_NUMBER}
                *Git Commit:* ${gitCommitShort} | ${gitCommitMsg}
                *Author:* ${gitAuthor}
                *Duration:* ${buildDuration}
                *More Info:* <${env.BUILD_URL}|View Build> | <${env.BUILD_URL}console|Console Output>
                """
                
                slackSend(
                    channel: '#micro-service-pipeline',
                    color: COLOR_MAP[buildStatus],
                    message: slackMessage
                )
            }
        }
        
    }
}