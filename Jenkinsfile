pipeline {
    agent any

    environment {
        DOCKER_TOKEN = credentials('docker-token')
    }


    stages {

        stage('Limpiar Workspace') {
            steps {
                sh 'rm -rf task-app'
            }
        }

        stage('Clonar Repositorio') {
            steps {
                sh 'git clone -b main https://github.com/danielsanchez2024/task-app.git'
            }
        }

        stage('verificar version docker') {
            steps {
                sh 'docker --version'
            }
        }


        stage('Construir Imagen Docker') {
            steps {
                sh 'docker build -t task-app:latest ./app'
            }
        }


        stage('Tag para Docker Registry') {
            steps {
                sh 'docker tag task-app:latest danielsanchez18/task-app:latest'
            }
        }


        stage('Iniciar Sesión en Docker Registry') {
            steps {
                 sh 'echo 1193380373 | docker login -u danielsanchez18 --password-stdin'
            }
        }


        stage('Subir Imagen a Docker Registry') {
            steps {
                sh 'docker push danielsanchez18/task-app:latest'
            }
        }
    }

    post {
        success {
            echo 'La imagen fue construida y subida con éxito.'
        }
        failure {
            echo 'Hubo un error durante el proceso.'
        }
    }
}
