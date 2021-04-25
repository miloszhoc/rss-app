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
                script {
                    sh 'python3.8 -m pytest tests/unit_tests  --junitxml=unit_result.xml'
                    junit 'unit_result.xml'
                }
            }
        }
        stage('integration_tests') {
            steps {
                script {
                    sh 'python3.8 -m pytest tests/integration_tests --junitxml=integration_result.xml'
                    junit 'integration_result.xml'
                }
            }
        }
        stage('deployment'){
            steps{
                sshPublisher failOnError: true, publishers: [sshPublisherDesc(configName: 'linux-vm', sshCredentials: [encryptedPassphrase: '{AQAAABAAQwl7TEcvDDLhdCHp1PPRDLqL8PbsXtxL8ViBycFtT/ps=}', key: '', keyPath: '', username: 'prod'], transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'cd rss-prod && docker-compose build && docker-compose up -d', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: 'rss-prod/', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '**', usePty: true)], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: true)]
            }
        }

        stage('e2e_tests') {
            steps {
                script {
                    sh 'python3.8 -m pytest tests/e2e_tests --html=report_e2e.html --self-contained-html --junitxml=e2e_result.xml'
                    junit 'e2e_result.xml'
                }
            }
        }
    }
    post {
        always { archiveArtifacts 'report_e2e.html'}
        cleanup { cleanWs() }
    }
}
