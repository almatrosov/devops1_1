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

        stage('Pre-Build: Unit Tests') {
            steps {
                echo 'Запуск юнит-тестов бэкенда (проверка исходного кода)...'
                # Создаем изолированное окружение на хосте внутри воркспейса Jenkins и запускаем тесты
                sh '''                    python3 -m venv test_venv                    ./test_venv/bin/pip install -r backend/requirements.txt                    ./test_venv/bin/python backend/test_app.py                '''
            }
        }

        stage('Docker Deploy') {
            steps {
                echo 'Юнит-тесты пройдены. Развертывание приложения...'
                sh 'docker compose -p project1 down'
                sh 'docker compose -p project1 up -d --build'
            }
        }

        stage('Post-Build: Smoke Tests') {
            steps {
                echo 'Проверка собранных и запущенных артефактов (Smoke Test)...'
                # Даем контейнерам 5 секунд на полную инициализацию и запуск веб-серверов
                sleep 5

                echo 'Тестируем доступность фронтенда через Nginx...'
                sh '''                    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/)                    echo "Nginx Frontend HTTP Status: $STATUS_CODE"                    if [ "$STATUS_CODE" -ne 200 ]; then                        echo "ОШИБКА: Фронтенд на порту 8081 вернул код $STATUS_CODE вместо 200!"                        exit 1                    fi                '''

                echo 'Тестируем доступность бэкенд API через балансировщик Nginx...'
                sh '''                    API_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/api/health)                    echo "Nginx Proxy to Backend API HTTP Status: $API_CODE"                    if [ "$API_CODE" -ne 200 ]; then                        echo "ОШИБКА: API бэкенда недоступен через прокси Nginx (Код: $API_CODE)!"                        exit 1                    fi                '''
                echo 'Все автоматические тесты успешно пройдены! Сборка валидна.'
            }
        }
    }
}