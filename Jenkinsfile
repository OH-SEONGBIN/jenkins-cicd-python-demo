pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/OH-SEONGBIN/jenkins-cicd-python-demo.git'
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
