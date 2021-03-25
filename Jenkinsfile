pipeline {
    agent { node { label 'docker' } }
    stages {
        stage('setup_env') {
            steps {
                sh 'python3.8 -m venv venv'
                sh 'source venv/bin/activate'
                sh 'python3.8 -m pip install -r requirements.txt'
            }
        }
        stage('check_code') {
            steps {
                sh 'bandit -r rss_app'
            }
        }
        stage('check_health') {
            steps {
                sh 'pytest tests/test__init__.py'
            }
        }
        stage('unit_tests') {
            steps {
                sh 'pytest tests/unit_tests'
            }
        }
        stage('integration_tests') {
            steps {
                sh 'pytest tests/integration_tests'
            }
        }
    }
}