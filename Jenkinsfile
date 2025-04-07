pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID = credentials('aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = credentials('aws_secret_access_key')
        AWS_DEFAULT_REGION = 'us-east-1'
    }
    stages{
        stage("Deploy Example Deployment") {
            steps {
                script {
                    sh "kubectl apply -f https://k8s.io/examples/controllers/nginx-deployment.yaml"
                }
            }
        }
    }   
}
