pipeline {
    agent any

    triggers {
        // Опрашивать GitHub на наличие новых коммитов каждую минуту
        pollSCM('* * * * *')
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Очищаем рабочую директорию перед сборкой
                cleanWs()
                // Скачиваем актуальный код из Git
                checkout scm
            }
        }

        stage('Docker Deploy') {
            steps {
                echo 'Перезапускаем контейнеры команды project_01...'
                // Явно указываем имя проекта через -p, чтобы перетереть прошлый деплой
                sh 'docker compose -p project_01 down'
                sh 'docker compose -p project_01 up -d --build'
            }
        }
    }
}
