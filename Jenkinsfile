pipeline {
    agent any

    triggers {
        // перевіряти репозиторій на нові коміти щохвилини
        pollSCM('* * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python --version
                    pip install -q -r requirements.txt
                '''
            }
        }
        stage('Run tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --cov=healthyday --cov=math_module --cov-report=term-missing --junitxml=test-results.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
        }
        success {
            echo 'Усі тести пройдено — збірку можна інтегрувати.'
        }
        failure {
            echo 'Є тести, що не пройшли — інтеграцію зупинено.'
        }
    }
}
