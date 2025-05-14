pipeline {
    agent any

    stages {
        stage('Sync') {
            steps {
                sh 'python3 --version'
                sh 'python3 ci-scripts/00_repo_sync.py'
            }
        }

        stage('Update SRCREV') {
            steps {
                sh 'python3 ci-scripts/01_update_revs.py'
            }
        }

        stage('Build') {
            steps {
                // Pass to build script the path to workspace to build
                sh 'python3 ci-scripts/02_build_image.py this/is/path'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}

