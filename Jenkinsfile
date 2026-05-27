pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Checkout Code') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Docker Deploy') {
            steps {
                echo 'Управляем контейнерами проекта project1...'
                sh 'docker compose -p project1 down'
                sh 'docker compose -p project1 up -d --build'
            }
        }
    }
}