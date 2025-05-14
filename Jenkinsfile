pipeline {
    agent any

    stages {
        stage('Sync') {
            steps {
                sh 'python3 --version'
                sh 'python3 ci-scripts/00_repo_sync.py'
            }
        }

        stage('Build') {
            steps {
                echo 'Building..'
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

