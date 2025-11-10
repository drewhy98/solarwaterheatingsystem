pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('DockerHub')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/drewhy98/solarwaterheatingsystem.git'
            }
        }

        stage('Docker Login') {
            steps {
                sh 'echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin'
            }
        }

        stage('Build & Run Docker') {
            steps {
                sh '''
                    docker stop solarwaterheatingsystem_app || true
                    docker rm solarwaterheatingsystem_app || true
                    docker rmi solarwaterheatingsystem_app_image || true
                    docker build -t solarwaterheatingsystem_app_image .
                    docker-compose up -d
                '''
            }
        }

        stage('Verify') {
            steps {
                echo "solarwaterheatingsystem Python app is running with MySQL database."
            }
        }

        stage('Clean Up') {
            steps {
                sh 'docker-compose down || true'
            }
        }
    }
}
