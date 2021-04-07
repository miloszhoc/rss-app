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
                sshPublisher failOnError: true, publishers: [sshPublisherDesc(configName: 'linux-vm', sshCredentials: [encryptedPassphrase: '{AQAAABAAQwl7TEcvDDLhdCHp1PPRDLqL8PbsXtxL8ViBycFtT/ps=}', key: '', keyPath: '', username: 'prod'], transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'cd rss-prod && docker-compose build && docker-compose up -d', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: 'rss-prod/', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**', usePty: true)], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: true)]
            }
        }

        stage('e2e_tests') {
            steps {
                sh 'python3.8 -m pytest tests/e2e_tests'
            }
        }
    }
}