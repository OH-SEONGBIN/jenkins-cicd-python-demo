pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/OH-SEONGBIN/my-python-project.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install pytest'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
    }
}