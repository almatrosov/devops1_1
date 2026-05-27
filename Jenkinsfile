pipeline {
    agent any

    triggers {
        // Опрашивать репозиторий на наличие новых коммитов каждую минуту
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
                echo 'Перезапускаем контейнеры с новым кодом...'
                sh 'docker compose down'
                sh 'docker compose up -d --build'
            }
        }
    }
}