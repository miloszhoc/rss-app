pipeline {
    agent { node { label 'docker' } }
//    environment {
//        FLASK_APP = credentials('FLASK_APP')
//        FLASK_ENV = credentials('FLASK_ENV')
//        CONFIG = credentials('CONFIG')
//        DB_HOST = credentials('DB_HOST')
//        DB_USER = credentials('DB_USER')
//        DB_PASS = credentials('DB_PASS')
//        DB_NAME = credentials('DB_NAME')
//        DB_TABLE = credentials('DB_TABLE')
//        DB_PORT = credentials('DB_PORT')
//        SENDGRID_KEY = credentials('SENDGRID_KEY')
//        FROM_EMAIL = credentials('FROM_EMAIL')
//    }
    stages {
        stage('setup_env') {
            steps {
                sh 'python3.8 -m pip install -r requirements.txt'
            }
        }
        stage('check_code') {
            steps {
                sh 'chmod 777 ./tests/check_code_bandit.py'
                sh 'python3.8 -m bandit -r rss_app -q | ./tests/check_code_bandit.py'
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
        stage('deployment'){
            steps{
                sshPublisher(publishers: [sshPublisherDesc(configName: 'linux-vm', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'docker-compose up -d', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: 'rss_app/*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
            }
        }
        stage('e2e_tests') {
            steps {
                sh 'python3.8 -m pytest tests/e2e_tests'
            }
        }
    }
}