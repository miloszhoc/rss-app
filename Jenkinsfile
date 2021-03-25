pipeline {
    agent { node { label 'docker' } }
    stages {
        stage('setup_env') {
            steps {
                sh 'python3.8 -m pip install -r requirements.txt'
            }
        }
        stage('check_code') {
            steps {
                sh 'python3.8 -m bandit -r rss_app'
            }
        }
        stage('check_health') {
            steps {
                sh 'python3.8 -m pytest tests/test__init__.py'
            }
        }
        stage('unit_tests') {
            steps {
                sh 'python3.8 -m pytest tests/unit_tests'
            }
        }
        stage('integration_tests') {
            steps {
                sh 'python3.8 -m pytest tests/integration_tests'
            }
        }
    }
}