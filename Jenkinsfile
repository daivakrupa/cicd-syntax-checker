pipeline {
    agent any

    stages {

        stage('Build') {

            steps {
                echo 'Building application'
            }

        }

        stage('Test') {

            step {    // INVALID: should be "steps"
                echo 'Running tests'
            }

        }

        stage('Deploy') {

            steps {
                echo 'Deploying application';
            }

        }

    }
}
